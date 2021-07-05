export async const fetchSendMessage = (url) => {
    const send = await fetch(url)
    if (!send.ok) {
       throw new Error(`Ваш запрос не выполнен.Ошибка сервера.попробуйте повторить запрос`)
    } 
    return send

};