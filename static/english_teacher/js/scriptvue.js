import fetchSendMessage from './api.js';
let jsDomain = JSON.parse(document.getElementById('domain-test').textContent);
const App = {

    data() {
        return {
            jsDomain,
            nameReview: '',
            textReview: '',
            emailText: '',
            messageText: '',
            SendMessage: 'Ваше сообщение успешно отправленно!',
            SendIsActive: true,
            isActive: true,
            isActiveCall: true,
            isActiveMessage: true,
            successMessage: true,
            successMessageReview: true,
            errorMessage: true,
            sendRewiew: true,
            sendOneMessage: true,
            errorMessageReview: true,
            sendMessageForm: 'inline',
            reviews: [],
        }
    },
    methods: {
        domainTest() {
            console.log(jsDomain)
        },
        format_date(value){
            return moment(String(value)).format('MMMM Do YYYY, h:mm a')
        },
        showReviews() {
            this.isActive = !this.isActive

        },
        successMessageClose() {
            this.errorMessageReview = true
            this.successMessageReview = true
            this.successMessage = true
            this.isActiveMessage = true
            this.errorMessage = true
            this.sendMessageForm = 'inline'
        },
        showCall() {
            console.log('ShowReviews')
            this.isActiveCall = !this.isActiveCall
        },
        showMessage() {
            this.isActiveMessage = !this.isActiveMessage
        },
        getReviews() {
            const vm = this;
            axios.get(`https://privatenglishtutor.ru/api/review`)
            .then(function(response){
                vm.reviews = response.data
            });
        },

        successFunc() {
            this.successMessage = !this.successMessage
        },
        
        errorFunc() {
            this.errorMessage = !this.errorMessage
            this.sendMessageForm = 'none'
        },
        errorFuncReview() {
            this.errorMessageReview = !this.errorMessageReview
        },
        inputEmailText(event) {
            this.emailText = event.target.value
        },
        inputMessageText(event) {
            this.messageText = event.target.value
        },
        successReviewFunc() {
            this.successMessageReview = !this.successMessageReview
        },
        closeAlertTime(displayActive) {
            if (displayActive == false) {
                setTimeout(() => {
                    this.successMessageClose()
                }, 8000)
            } 
        },
        addReview() {
            this.sendRewiew = false
            let csrftoken = Cookies.get('csrftoken');
            let datas = {
                email: this.nameReview,
                message: this.textReview
            }
            fetchSendMessage(`https://privatenglishtutor.ru/send_message/review/${this.nameReview}/${this.textReview}`)
            .then(data => data.text())
            .then(data => {
                this.sendRewiew = true
                this.successReviewFunc()
                this.closeAlertTime(this.successMessageReview)

            }).catch(() => {
                this.errorFuncReview()
                this.closeAlertTime(this.errorMessageReview)
                this.sendRewiew = true


            }).finally(() => {
                this.sendRewiew = true
                console.log(jsDomain)
                this.nameReview = ''
                this.textReview = ''

            });
        },
        // async fetchSendMessage(url) {
        //     const send = await fetch(url)
        //     if (!send.ok) {
        //        throw new Error(`Ваш запрос не выполнен.Ошибка сервера.попробуйте повторить запрос`)
        //     } 
        //     return send

        // },

        sendMessage() {
            if ((this.emailText).length == 0 || (this.messageText).length == 0 ||
                 this.emailText == undefined || this.messageText == undefined ||
                 this.emailText.indexOf('@') == -1) {
                alert('Ваше сообщение не может быть отправлено.Проверьте заполненные вами данные')
            }
            else {
                this.sendOneMessage = false
                fetchSendMessage(`https://privatenglishtutor.ru/send_message/message/${this.emailText}/${this.messageText}`)                

                .then(response => response.text())
                .then(() => {
                    this.successFunc()
                    this.sendOneMessage = true
                    this.closeAlertTime(this.successMessage)
                })
                .catch(() => {
                    this.errorFunc()
                    // this.errorMessage = false
                    this.sendOneMessage = true
                    this.closeAlertTime(this.errorMessage)
                    console.log('error')
                }).finally(() => {
                    console.log('finally')
                    this.sendMessageForm = 'none'
                    this.sendOneMessage = true
                });
            }
            
    
        },
        inputReviewName(event) {
            this.nameReview = event.target.value
        },
        inputReviewText(event) {
            this.textReview = event.target.value
        },


    },
    created() {
        this.getReviews();
    }

}

Vue.createApp(App).mount('#reviews', '#footer_vue')
