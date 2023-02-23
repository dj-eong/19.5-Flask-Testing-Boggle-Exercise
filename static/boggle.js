const form = document.querySelector('form');
const input = document.querySelector('#guess');
const main = document.querySelector('main');

form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const config = { params: { guess: input.value } };
    const res = await axios.get('/process-guess', config);

    const div = document.createElement('div');
    div.innerText = res.data.result;
    main.append(div);
});
console.log('please...');