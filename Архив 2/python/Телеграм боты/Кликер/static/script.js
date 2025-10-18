const colors = [
    '#0b1d4f', // тёмно-синий
    '#1e3a8a', // синий
    '#2563eb', // ярко-синий
    '#4c51bf', // сине-фиолетовый
    '#2d3748', // тёмно-серый
    '#1a202c', // очень тёмный
    '#3b82f6', // голубой
    '#4338ca'  // фиолетовый
];

let count = 0;
const button = document.getElementById('clicker-button');

button.addEventListener('click', () => {
    // увеличиваем счётчик и обновляем текст кнопки
    count++;
    button.textContent = count;

    // меняем цвет фона рандомно (кроме текущего)
    let newColor;
    do {
        newColor = colors[Math.floor(Math.random() * colors.length)];
    } while (newColor === document.body.style.backgroundColor);
    document.body.style.backgroundColor = newColor;

    // отправляем ник пользователя на сервер
    const tg = window.Telegram.WebApp;
    fetch('/click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: tg.initDataUnsafe?.user?.username || 'неизвестно'
        })
    });
});
