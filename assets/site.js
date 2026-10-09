// Kynkr — site vitrine : menu mobile, apparition douce, formulaire « Me prévenir ».
(function () {
  'use strict';

  var FONCTION = 'https://byhudkuzmmngnnfiqpii.supabase.co/functions/v1/waitlist-signup';

  // Menu mobile
  var toggle = document.querySelector('.nav-toggle');
  var liens = document.querySelector('.nav-links');
  if (toggle && liens) {
    toggle.addEventListener('click', function () {
      var ouvert = liens.classList.toggle('open');
      toggle.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
    });
    liens.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        liens.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Apparition douce au défilement (le contenu reste visible sans JavaScript)
  var elements = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && elements.length) {
    var obs = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); obs.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    elements.forEach(function (el) { obs.observe(el); });
  } else {
    elements.forEach(function (el) { el.classList.add('in'); });
  }

  // Formulaires « Me prévenir »
  var MESSAGES = {
    ok: 'C’est noté ✨ On te prévient dès l’ouverture.',
    email: 'Cette adresse ne semble pas valide. Vérifie-la et réessaie.',
    limite: 'Trop de tentatives pour le moment. Réessaie dans une heure.',
    reseau: 'La connexion a flanché. Réessaie dans un instant.',
    serveur: 'Un imprévu de notre côté. Réessaie dans un instant.'
  };

  document.querySelectorAll('form.waitlist').forEach(function (form) {
    var champ = form.querySelector('input[type="email"]');
    var piege = form.querySelector('input[name="website"]');
    var bouton = form.querySelector('button[type="submit"]');
    var statut = form.parentNode.querySelector('.waitlist-status');
    var source = form.getAttribute('data-source') || 'site';

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var email = (champ.value || '').trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        montrer('err', MESSAGES.email);
        champ.focus();
        return;
      }
      bouton.disabled = true;
      var libelle = bouton.textContent;
      bouton.textContent = '…';

      fetch(FONCTION, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, website: piege ? piege.value : '', source: source })
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { status: r.status, json: j }; }); })
        .then(function (res) {
          if (res.json && res.json.ok) {
            montrer('ok', MESSAGES.ok);
            bouton.textContent = '✓';
            champ.value = '';
            champ.disabled = true;
          } else {
            var cle = res.json && res.json.error;
            montrer('err', MESSAGES[cle] || MESSAGES.serveur);
            bouton.disabled = false;
            bouton.textContent = libelle;
          }
        })
        .catch(function () {
          montrer('err', MESSAGES.reseau);
          bouton.disabled = false;
          bouton.textContent = libelle;
        });
    });

    function montrer(type, texte) {
      if (!statut) return;
      statut.className = 'waitlist-status ' + type;
      statut.textContent = texte;
    }
  });
})();
