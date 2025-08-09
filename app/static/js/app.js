// CV Builder Vue.js Application
const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    data() {
        return {
            isLoading: false,
            previewHTML: '',
            selectedTemplate: 'classic',
            templates: [],
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
        this.loadTemplates();
        this.loadSampleData();
        this.setupAutoSave();
    },

    methods: {
        async loadTemplates() {
            try {
                const response = await fetch('/api/templates');
                const data = await response.json();
                this.templates = data;
                if (data.length > 0) {
                    this.selectedTemplate = data[0].id;
                }
            } catch (error) {
                console.error('Error loading templates:', error);
                this.showNotification('Error loading templates', 'error');
            }
        },

        loadSampleData() {
            // Load sample data for demonstration
            this.resumeData = {
                basics: {
                    name: 'John Doe',
                    label: 'Software Engineer',
                    image: 'https://via.placeholder.com/150',
                    email: 'john.doe@example.com',
                    phone: '+1 (555) 123-4567',
                    url: 'https://linkedin.com/in/johndoe',
                    summary: 'Experienced software engineer with a passion for creating innovative solutions and leading development teams.',
                    location: {
                        address: '123 Main St',
                        postal_code: '12345',
                        city: 'San Francisco',
                        country_code: 'US',
                        region: 'California'
                    },
                    profiles: [{
                        network: 'LinkedIn',
                        username: 'johndoe',
                        url: 'https://linkedin.com/in/johndoe'
                    }]
                },
                work: [{
                    name: 'Tech Corp',
                    position: 'Senior Software Engineer',
                    url: 'https://techcorp.com',
                    start_date: '2020-01',
                    end_date: 'Current',
                    summary: 'Lead development of scalable web applications using modern technologies.',
                    highlights: []
                }],
                education: [{
                    institution: 'University of Technology',
                    url: 'https://university.edu',
                    area: 'Computer Science',
                    study_type: 'Bachelor',
                    start_date: '2015',
                    end_date: '2019',
                    score: '',
                    courses: []
                }],
                skills: [{
                    name: 'JavaScript',
                    level: '5',
                    keywords: ['React', 'Node.js', 'Vue.js'],
                    keywordsText: 'React, Node.js, Vue.js'
                }, {
                    name: 'Python',
                    level: '4',
                    keywords: ['Django', 'Flask', 'FastAPI'],
                    keywordsText: 'Django, Flask, FastAPI'
                }],
                volunteer: [],
                awards: [],
                publications: [],
                languages: [{
                    language: 'English',
                    fluency: { value: 'Native' }
                }, {
                    language: 'Spanish',
                    fluency: { value: 'Intermediate' }
                }],
                interests: [{
                    name: 'Photography'
                }, {
                    name: 'Travel'
                }],
                references: [],
                projects: []
            };
        },

        setupAutoSave() {
            // Auto-save to localStorage
            this.$watch('resumeData', (newVal) => {
                localStorage.setItem('cvBuilderData', JSON.stringify(newVal));
            }, { deep: true });

            // Load from localStorage if available
            const saved = localStorage.getItem('cvBuilderData');
            if (saved) {
                try {
                    const parsedData = JSON.parse(saved);
                    // Merge with default structure to ensure all fields exist
                    this.resumeData = this.mergeDeep(this.resumeData, parsedData);
                } catch (error) {
                    console.error('Error loading saved data:', error);
                }
            }
        },

        mergeDeep(target, source) {
            const output = Object.assign({}, target);
            if (this.isObject(target) && this.isObject(source)) {
                Object.keys(source).forEach(key => {
                    if (this.isObject(source[key])) {
                        if (!(key in target))
                            Object.assign(output, { [key]: source[key] });
                        else
                            output[key] = this.mergeDeep(target[key], source[key]);
                    } else {
                        Object.assign(output, { [key]: source[key] });
                    }
                });
            }
            return output;
        },

        isObject(item) {
            return item && typeof item === 'object' && !Array.isArray(item);
        },

        async previewCV() {
            this.isLoading = true;
            try {
                const response = await fetch('/api/preview', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        resume_data: this.prepareResumeData(),
                        template: this.selectedTemplate
                    })
                });

                const data = await response.json();
                if (data.success) {
                    this.previewHTML = data.html;
                } else {
                    this.showNotification(data.error || 'Error generating preview', 'error');
                }
            } catch (error) {
                console.error('Error generating preview:', error);
                this.showNotification('Error generating preview', 'error');
            } finally {
                this.isLoading = false;
            }
        },

        async refreshPreview() {
            if (this.previewHTML) {
                await this.previewCV();
            }
        },

        async downloadProject() {
            this.isLoading = true;
            try {
                const response = await fetch('/api/download-project', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        resume_data: this.prepareResumeData(),
                        template: this.selectedTemplate,
                        project_name: this.resumeData.basics.name.toLowerCase().replace(/\s+/g, '-') + '-cv' || 'my-cv-project'
                    })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${this.resumeData.basics.name.toLowerCase().replace(/\s+/g, '-')}-cv-project.zip`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    this.showNotification('Project downloaded successfully!', 'success');
                } else {
                    const data = await response.json();
                    this.showNotification(data.error || 'Error downloading project', 'error');
                }
            } catch (error) {
                console.error('Error downloading project:', error);
                this.showNotification('Error downloading project', 'error');
            } finally {
                this.isLoading = false;
            }
        },

        async exportPDF() {
            this.isLoading = true;
            try {
                const response = await fetch('/api/export-pdf', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        resume_data: this.prepareResumeData(),
                        template: this.selectedTemplate
                    })
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${this.resumeData.basics.name.toLowerCase().replace(/\s+/g, '-')}-resume.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    this.showNotification('PDF exported successfully!', 'success');
                } else {
                    const data = await response.json();
                    this.showNotification(data.error || 'Error exporting PDF', 'error');
                }
            } catch (error) {
                console.error('Error exporting PDF:', error);
                this.showNotification('Error exporting PDF', 'error');
            } finally {
                this.isLoading = false;
            }
        },

        prepareResumeData() {
            // Convert string levels to proper format for skills
            const preparedData = JSON.parse(JSON.stringify(this.resumeData));

            if (preparedData.skills) {
                preparedData.skills = preparedData.skills.map(skill => ({
                    ...skill,
                    level: { value: parseInt(skill.level) },
                    level_percent: parseInt(skill.level) * 20
                }));
            }

            if (preparedData.education) {
                preparedData.education = preparedData.education.map(edu => ({
                    ...edu,
                    study_type: { value: edu.study_type }
                }));
            }

            return preparedData;
        },

        // Dynamic form methods
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
                keywordsText: ''
            });
        },

        removeSkill(index) {
            this.resumeData.skills.splice(index, 1);
        },

        updateSkillKeywords(index) {
            const skill = this.resumeData.skills[index];
            skill.keywords = skill.keywordsText
                .split(',')
                .map(k => k.trim())
                .filter(k => k.length > 0);
        },

        showNotification(message, type = 'info') {
            // Simple notification system
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 24px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                animation: slideIn 0.3s ease;
                ${type === 'success' ? 'background: #38a169;' : ''}
                ${type === 'error' ? 'background: #e53e3e;' : ''}
                ${type === 'info' ? 'background: #3182ce;' : ''}
            `;

            document.body.appendChild(notification);

            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => {
                    document.body.removeChild(notification);
                }, 300);
            }, 3000);
        }
    }
}).mount('#app');

// Add CSS for notifications
const notificationCSS = `
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}
`;

const style = document.createElement('style');
style.textContent = notificationCSS;
document.head.appendChild(style);
