'use strict'

const inputEmail = document.querySelector('#exampleFormControlInput1'),
      inputLetter = document.querySelector('#exampleFormControlTextarea1'),
      btnSendLetter = document.querySelector('#sendMessage'),
      alertSuccess = document.querySelector('#alertSuccessId'),
      preloader = document.querySelector('.content'),
      alertMistake = document.querySelector('#alertMistakeId');
      
const fetchSendMessage = async (url) => {
    const send = await fetch(url)
    if (!send.ok) {
       throw new Error(`Ваш запрос не выполнен.Ошибка сервера.попробуйте повторить запрос`)
    } 
    return send
}; 
const funSuccess = () => {
    alertSuccess.style.display = 'block'
    setTimeout(funSuccessNone, 5000)  
};
const funSuccessNone = () => {
    alertSuccess.style.display = 'none';
};
const funMistake = () => {
    alertMistake.style.display = 'block';
};
const funMistakeNone = () => {
    alertMistake.style.display = 'none';
    setTimeout(funSuccessNone, 5000)  
};
const funpreloaderShow = () => {
    preloader.style.display = 'block'
};

const funpreloaderFade = () => {
    preloader.style.display = 'none'
};

btnSendLetter.addEventListener('click', ()=> {
    if ((inputEmail.value).length == 0 || (inputLetter.value).length == 0 ||
        inputEmail.value == undefined || inputLetter.value == undefined ||
        inputEmail.value.indexOf('@') == -1) {
    btnSendLetter.classList.remove('fly')
    alert('Ваше сообщение не может быть отправлено.Проверьте заполненные вами данные')
    }else {
        funpreloaderShow();
        fetchSendMessage(`https://privatenglishtutor.ru/send_message/message/${inputEmail.value}/${inputLetter.value}`)
        .then(() => {
            funpreloaderFade();
            funSuccess();            
        }).catch(() => {
            funpreloaderFade();
            funMistake();
        })
    }
});