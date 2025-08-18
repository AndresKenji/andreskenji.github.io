const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'], // Cambio los delimitadores para evitar conflicto con Jinja2
    data() {
        return {
            isLoading: false,
            selectedTemplate: 'classic',
            templates: [],
            previewHTML: '',
            showSuccessMessage: false,
            showErrorMessage: false,
            successMessage: '',
            errorMessage: '',
            resumeData: {
                basics: {
                    name: '',
                    label: '',
                    image: '',
                    email: '',
                    phone: '',
                    url: '',
                    summary: '',
                    location: {
                        address: '',
                        postal_code: '',
                        city: '',
                        country_code: '',
                        region: ''
                    },
                    profiles: []
                },
                work: [],
                education: [],
                skills: [],
                volunteer: [],
                awards: [],
                publications: [],
                languages: [],
                interests: [],
                references: [],
                projects: []
            }
        }
    },

    mounted() {
        console.log('Vue app mounted');
        this.loadTemplates();
        this.loadDataFromFile();
        this.setupAutoSave();
    },

    methods: {
        async loadTemplates() {
            console.log('Loading templates...');
            try {
                const response = await fetch('/api/templates');
                console.log('Templates response:', response);
                const data = await response.json();
                console.log('Templates data:', data);
                this.templates = data;
                console.log('Templates loaded:', this.templates);
            } catch (error) {
                console.error('Error loading templates:', error);
                this.showError('Error loading templates');
            }
        },

        async loadDataFromFile() {
            console.log('Loading data from src/data/resume.json...');
            try {
                const response = await fetch('/api/load-data');
                if (response.ok) {
                    const data = await response.json();
                    if (data.success && data.data) {
                        this.resumeData = { ...this.resumeData, ...data.data };
                        console.log('Data loaded from file:', this.resumeData);
                        this.refreshPreview();
                    }
                }
            } catch (error) {
                console.log('No existing data file found, starting with empty form');
            }
        },

        async saveDataToFile() {
            try {
                const response = await fetch('/api/save-data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        resume_data: this.prepareResumeData()
                    }),
                });

                const data = await response.json();
                if (data.success) {
                    console.log('Data saved to src/data/resume.json');
                } else {
                    console.error('Error saving data:', data.error);
                }
            } catch (error) {
                console.error('Error saving data to file:', error);
            }
        },

        async refreshPreview() {
            if (!this.validateBasicFields()) {
                this.previewHTML = '';
                return;
            }

            this.isLoading = true;

            try {
                // Guardar datos automáticamente antes de generar preview
                await this.saveDataToFile();

                const response = await fetch('/api/preview', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        resume_data: this.prepareResumeData(),
                        template: this.selectedTemplate
                    }),
                });

                const data = await response.json();

                if (data.success) {
                    this.previewHTML = data.html;
                } else {
                    console.error('Preview errors:', data.errors || data.error);
                    this.showError(data.error || 'Error generating preview');
                    this.previewHTML = '';
                }
            } catch (error) {
                console.error('Error generating preview:', error);
                this.showError('Network error generating preview');
                this.previewHTML = '';
            } finally {
                this.isLoading = false;
            }
        },

        loadPreview() {
            // Llamado cuando cambia el template
            if (this.validateBasicFields()) {
                this.refreshPreview();
            }
        },

        async generateFinalCV() {
            if (!this.validateBasicFields()) {
                return;
            }

            if (!confirm('This will generate your final CV and save it to the GitHub Pages. Are you sure?')) {
                return;
            }

            this.isLoading = true;
            this.showSuccessMessage = false;
            this.showErrorMessage = false;

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        resume_data: this.prepareResumeData(),
                        template: this.selectedTemplate
                    }),
                });

                const data = await response.json();

                if (data.success) {
                    this.showSuccess('CV generated and saved to docs/index.html successfully! Your GitHub Pages will be updated.');
                } else {
                    console.error('Generation errors:', data.errors || data.error);
                    this.showError(data.error || 'Error generating final CV');
                }
            } catch (error) {
                console.error('Error generating final CV:', error);
                this.showError('Network error generating final CV');
            } finally {
                this.isLoading = false;
            }
        },

        async exportPDF() {
            if (!this.validateBasicFields()) {
                return;
            }

            this.isLoading = true;
            this.showSuccessMessage = false;
            this.showErrorMessage = false;

            try {
                const response = await fetch('/api/generate-pdf', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        resume_data: this.prepareResumeData(),
                        template: this.selectedTemplate
                    }),
                });

                const data = await response.json();

                if (data.success) {
                    this.showSuccess('PDF generated successfully in docs/resume.pdf!');
                } else {
                    console.error('PDF generation errors:', data.errors || data.error);
                    this.showError(data.error || 'Error generating PDF');
                }
            } catch (error) {
                console.error('Error generating PDF:', error);
                this.showError('Network error generating PDF');
            } finally {
                this.isLoading = false;
            }
        },

        prepareResumeData() {
            // Crear una copia profunda para no modificar los datos originales
            const data = JSON.parse(JSON.stringify(this.resumeData));

            // Asegurar que las listas vacías estén inicializadas
            if (!data.work) data.work = [];
            if (!data.education) data.education = [];
            if (!data.skills) data.skills = [];
            if (!data.languages) data.languages = [];
            if (!data.interests) data.interests = [];
            if (!data.volunteer) data.volunteer = [];
            if (!data.awards) data.awards = [];
            if (!data.publications) data.publications = [];
            if (!data.references) data.references = [];
            if (!data.projects) data.projects = [];

            // Convertir los niveles de skills al formato esperado por el modelo
            data.skills = data.skills.map(skill => ({
                ...skill,
                level: this.convertSkillLevel(skill.level),
                keywords: skill.keywords || []
            }));

            // Convertir languages al formato esperado
            data.languages = data.languages.map(lang => ({
                ...lang,
                fluency: lang.fluency || 'Intermediate'
            }));

            return data;
        },

        convertSkillLevel(level) {
            const levelMap = {
                '1': 'Novice',
                '2': 'Competent',
                '3': 'Competent',
                '4': 'Proficient',
                '5': 'Master'
            };
            return levelMap[level] || 'Competent';
        },

        validateBasicFields() {
            if (!this.resumeData.basics.name) {
                this.showError('Please enter your name');
                return false;
            }
            if (!this.resumeData.basics.email) {
                this.showError('Please enter your email');
                return false;
            }
            if (!this.resumeData.basics.label) {
                this.showError('Please enter your professional title');
                return false;
            }
            return true;
        },

        showSuccess(message) {
            this.successMessage = message;
            this.showSuccessMessage = true;
            this.showErrorMessage = false;
            setTimeout(() => {
                this.showSuccessMessage = false;
            }, 5000);
        },

        showError(message) {
            this.errorMessage = message;
            this.showErrorMessage = true;
            this.showSuccessMessage = false;
            setTimeout(() => {
                this.showErrorMessage = false;
            }, 5000);
        },

        // Métodos para manejar arrays dinámicos
        addWork() {
            this.resumeData.work.push({
                name: '',
                position: '',
                url: '',
                start_date: '',
                end_date: '',
                summary: '',
                highlights: []
            });
        },

        removeWork(index) {
            this.resumeData.work.splice(index, 1);
        },

        addEducation() {
            this.resumeData.education.push({
                institution: '',
                url: '',
                area: '',
                study_type: 'Bachelor',
                start_date: '',
                end_date: '',
                score: '',
                courses: []
            });
        },

        removeEducation(index) {
            this.resumeData.education.splice(index, 1);
        },

        addSkill() {
            this.resumeData.skills.push({
                name: '',
                level: '3',
                keywords: [],
                keywordsText: '',
                color: '#0070c0'
            });
        },

        removeSkill(index) {
            this.resumeData.skills.splice(index, 1);
        },

        updateSkillKeywords(index) {
            const keywordsText = this.resumeData.skills[index].keywordsText || '';
            this.resumeData.skills[index].keywords = keywordsText
                .split(',')
                .map(k => k.trim())
                .filter(k => k.length > 0);
        },

        addLanguage() {
            this.resumeData.languages.push({
                language: '',
                fluency: 'Intermediate'
            });
        },

        removeLanguage(index) {
            this.resumeData.languages.splice(index, 1);
        },

        addInterest() {
            this.resumeData.interests.push({
                name: '',
                keywords: []
            });
        },

        removeInterest(index) {
            this.resumeData.interests.splice(index, 1);
        },

        addVolunteer() {
            this.resumeData.volunteer.push({
                organization: '',
                position: '',
                url: '',
                start_date: '',
                end_date: '',
                summary: '',
                highlights: []
            });
        },

        removeVolunteer(index) {
            this.resumeData.volunteer.splice(index, 1);
        },

        addAward() {
            this.resumeData.awards.push({
                title: '',
                date: '',
                awarder: '',
                summary: ''
            });
        },

        removeAward(index) {
            this.resumeData.awards.splice(index, 1);
        },

        addPublication() {
            this.resumeData.publications.push({
                name: '',
                publisher: '',
                release_date: '',
                url: '',
                summary: ''
            });
        },

        removePublication(index) {
            this.resumeData.publications.splice(index, 1);
        },

        addReference() {
            this.resumeData.references.push({
                name: '',
                reference: ''
            });
        },

        removeReference(index) {
            this.resumeData.references.splice(index, 1);
        },

        addProject() {
            this.resumeData.projects.push({
                name: '',
                description: '',
                highlights: [],
                keywords: [],
                start_date: '',
                end_date: '',
                url: '',
                roles: [],
                entity: '',
                type: ''
            });
        },

        removeProject(index) {
            this.resumeData.projects.splice(index, 1);
        },

        addProfile() {
            this.resumeData.basics.profiles.push({
                network: '',
                username: '',
                url: ''
            });
        },

        removeProfile(index) {
            this.resumeData.basics.profiles.splice(index, 1);
        },

        setupAutoSave() {
            // Guardar datos cada 30 segundos tanto en localStorage como en archivo
            setInterval(() => {
                localStorage.setItem('cvBuilderData', JSON.stringify(this.resumeData));
                this.saveDataToFile();
            }, 30000);

            // Cargar datos guardados al iniciar (localStorage como backup)
            const savedData = localStorage.getItem('cvBuilderData');
            if (savedData) {
                try {
                    const parsed = JSON.parse(savedData);
                    // Solo cargar localStorage si no hay datos del archivo
                    if (!this.resumeData.basics.name && parsed.basics && parsed.basics.name) {
                        this.resumeData = { ...this.resumeData, ...parsed };
                        console.log('Data loaded from localStorage as fallback');
                    }
                } catch (error) {
                    console.error('Error loading saved data from localStorage:', error);
                }
            }

            // Auto-refresh preview cuando cambian los datos básicos
            this.$watch('resumeData.basics.name', () => {
                if (this.resumeData.basics.name && this.resumeData.basics.email) {
                    setTimeout(() => this.refreshPreview(), 1000);
                }
            });

            this.$watch('selectedTemplate', () => {
                if (this.validateBasicFields()) {
                    this.refreshPreview();
                }
            });
        },

        clearAllData() {
            if (confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
                localStorage.removeItem('cvBuilderData');
                location.reload();
            }
        }
    }
}).mount('#app');
