(function(){
  const form = document.getElementById('calcForm');
  const aEl = document.getElementById('a');
  const bEl = document.getElementById('b');
  const opEl = document.getElementById('op');
  const resultEl = document.getElementById('result');

  function show(text, isError){
    resultEl.style.display = 'block';
    resultEl.textContent = text;
    resultEl.style.background = isError ? '#fff0f0' : '';
    resultEl.style.borderColor = isError ? '#ffcccc' : '';
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    const a = parseFloat(aEl.value.trim());
    const b = parseFloat(bEl.value.trim());
    const op = opEl.value;

    if (Number.isNaN(a) || Number.isNaN(b)){
      show('Please enter valid numbers for both inputs.', true);
      return;
    }

    let r;
    switch(op){
      case 'add': r = a + b; break;
      case 'sub': r = a - b; break;
      case 'mul': r = a * b; break;
      case 'div':
        if (b === 0){ show('Cannot divide by zero', true); return; }
        r = a / b;
        break;
      default: show('Unknown operation', true); return;
    }

    show('Result: ' + r);
  });
})();