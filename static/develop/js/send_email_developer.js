import fetchSendMessage from '../../english_teacher/js/api.js';

const App = {
    
    data() {
        return {
            emailText: '',
            messageText: '',
            addMoveSendMessage: false,
            preloaderActive: true,
            textMessageHide: false,
        }

    },

    methods: {
        showAnimateSendMEssage() {
            this.addMoveSendMessage = !this.addMoveSendMessage
        },
        changeStateSendMessage() {
            this.preloaderActive = !this.preloaderActive
            this.textMessageHide = !this.textMessageHide

        },
        inputEmailText(event) {
            this.emailText = event.target.value
        },
        inputMessageText(event) {
            this.messageText = event.target.value
        },
        sendMessage() {
            if ((this.emailText).length == 0 || (this.messageText).length == 0 ||
                 this.emailText == undefined || this.messageText == undefined ||
                 this.emailText.indexOf('@') == -1) {
                alert('Ваше сообщение не может быть отправлено.Проверьте заполненные вами данные')
            }
            else {
                this.sendOneMessage = false
                this.changeStateSendMessage()
                fetchSendMessage(`https://privatenglishtutor.ru/send_message/message/${this.emailText}/${this.messageText}`)        

                .then(response => response.text())                
                .then(() => {
                    this.showAnimateSendMEssage()
                    setTimeout(() => {
                        this.showAnimateSendMEssage()
                    }, 4000)
                })
                .catch(() => {
                    alert('Ваше сообщение не отправленно! Ошибка сервера. Попробуйте позже')
                }).finally(() => {
                    setTimeout(() => {
                        this.changeStateSendMessage()
                    }, 3000)
                });
            }
        },

    },
    created() {

    }

}

Vue.createApp(App).mount('#mc_embed_signup')