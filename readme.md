# pip freeze > requirements.txt

# Instalar librerias
pip install -r requirements.txt

# Ademas de la libreria playwright, hay que instalar los navegadores en el global
# ..\Users\<TU_USUARIO>\AppData\Local\ms-playwright
playwright install

# Para la consola del browser:
# Buscar los inputs
const main = document.querySelector('main');
const fields = main.querySelectorAll('[role="textbox"], input, textarea, [contenteditable="true"]');
fields.forEach((el, i) => {
  console.log(i, el.tagName, el.getAttribute('name'), el.getAttribute('id'), el.getAttribute('role'), el.textContent);
});

# Buscar botones
const elements = document.querySelectorAll('button, input[type="button"], input[type="submit"], a');
elements.forEach((el, i) => {
  const role = el.getAttribute('role') || '';
  const text = el.innerText || el.value || '';
  console.log(`${i}: tag=${el.tagName}, role=${role}, text="${text.trim()}"`);
});


playwright codegen --target=python https://qa.syndication.wbd.com
playwright codegen --target=python https://file-mover.dev.neo-dev.wbd.com/
playwright codegen --target=python --viewport-size=1920,1080 https://file-mover.dev.neo-dev.wbd.com/
