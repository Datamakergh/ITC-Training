(function(){
  if(location.search.indexOf('embed')>-1){document.body.classList.add('embed');}

  const slides = Array.from(document.querySelectorAll('.slide'));
  const total = slides.length;
  const NUM_OFFSET = __NUM_OFFSET__;          // slides in the deck(s) before this one on the same day
  const OTHER_DECK_SLIDES = __OTHER__;     // slides in the deck(s) after this one on the same day
  const GRAND_TOTAL = NUM_OFFSET + total + OTHER_DECK_SLIDES;
  slides.forEach((s,i)=>{ const el=s.querySelector('.slide-num'); if(el){ el.setAttribute('data-n', i+1+NUM_OFFSET); el.setAttribute('data-total', GRAND_TOTAL); } });
  const overviewGrid = document.getElementById('overviewGrid');
  if(overviewGrid){
    slides.forEach((s,i)=>{
      const thumb = document.createElement('div');
      thumb.className = 'thumb';
      thumb.dataset.i = i;
      const n = document.createElement('span'); n.className = 'n'; n.textContent = String(i+1).padStart(2,'0');
      const t = document.createElement('span'); t.className = 't'; t.textContent = s.getAttribute('data-title') || '';
      thumb.append(n,t);
      overviewGrid.appendChild(thumb);
    });
  }
  let cur = 0;
  const bar = document.querySelector('.progress-bar > span');
  function render(){
    slides.forEach((s,i)=>{
      s.classList.remove('is-active','is-prev');
      if(i===cur) s.classList.add('is-active');
      else if(i<cur) s.classList.add('is-prev');
    });
    if(bar) bar.style.width = ((cur+1)/total*100)+'%';
    history.replaceState(null,'','#'+(cur+1));
  }
  function go(n){ cur = Math.max(0, Math.min(total-1, n)); render(); }
  const hash = parseInt((location.hash||'').replace('#',''),10);
  cur = (hash>=1 && hash<=total) ? hash-1 : 0;
  render();

  const notesOverlay = document.getElementById('notesOverlay');
  let notesOn = false;
  function updateNotes(){
    if(!notesOn) return;
    const n = slides[cur].querySelector('.notes');
    notesOverlay.querySelector('.nl-body').textContent = n ? n.textContent : '';
  }
  document.addEventListener('keydown', (e)=>{
    if(e.key==='ArrowRight' || e.key===' ' || e.key==='PageDown'){ go(cur+1); updateNotes(); }
    else if(e.key==='ArrowLeft' || e.key==='PageUp'){ go(cur-1); updateNotes(); }
    else if(e.key==='Home'){ go(0); updateNotes(); }
    else if(e.key==='End'){ go(total-1); updateNotes(); }
    else if(e.key.toLowerCase()==='n'){ notesOn=!notesOn; notesOverlay.classList.toggle('open',notesOn); updateNotes(); }
    else if(e.key.toLowerCase()==='o' || e.key==='Escape'){
      const ov = document.getElementById('overviewGrid');
      if(e.key==='Escape'){ ov.classList.remove('open'); return; }
      ov.classList.toggle('open');
    }
    else if(e.key.toLowerCase()==='f'){ document.documentElement.requestFullscreen && document.documentElement.requestFullscreen(); }
  });
  document.querySelectorAll('.overview .thumb').forEach(t=>{
    t.addEventListener('click', ()=>{ go(parseInt(t.dataset.i,10)); document.getElementById('overviewGrid').classList.remove('open'); updateNotes(); });
  });
  let touchX=null;
  document.addEventListener('touchstart', e=>touchX=e.touches[0].clientX);
  document.addEventListener('touchend', e=>{
    if(touchX===null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if(dx<-40) go(cur+1); else if(dx>40) go(cur-1);
    touchX=null;
  });

  function buildNotePages(){
    document.querySelectorAll('.deck > .slide').forEach(slide=>{
      if(slide.nextElementSibling && slide.nextElementSibling.classList && slide.nextElementSibling.classList.contains('note-page')) return;
      const notesEl = slide.querySelector('.notes');
      const text = notesEl ? notesEl.textContent.trim() : '';
      if(!text) return;
      const title = slide.getAttribute('data-title') || '';
      const numEl = slide.querySelector('.slide-num');
      const num = numEl ? numEl.getAttribute('data-n') : '';
      const np = document.createElement('div');
      np.className = 'note-page';
      const eyebrow = document.createElement('div'); eyebrow.className = 'np-eyebrow'; eyebrow.textContent = 'Speaker Notes: Slide ' + num;
      const h3 = document.createElement('h3'); h3.textContent = title;
      const p = document.createElement('p'); p.textContent = text;
      np.append(eyebrow, h3, p);
      slide.insertAdjacentElement('afterend', np);
    });
  }
  buildNotePages();

  const printToggle = document.getElementById('printNotesToggle');
  const printBtn = document.getElementById('printBtn');
  if(printToggle) printToggle.addEventListener('change', ()=>{ document.body.classList.toggle('print-with-notes', printToggle.checked); });
  if(printBtn) printBtn.addEventListener('click', ()=>window.print());
  const printPanel = document.getElementById('printPanel');
  const printPanelCollapse = document.getElementById('printPanelCollapse');
  if(printPanelCollapse) printPanelCollapse.addEventListener('click', ()=>{
    const collapsed = printPanel.classList.toggle('collapsed');
    printPanelCollapse.innerHTML = collapsed ? '&#9652; Print' : '&#9662;';
  });
})();
