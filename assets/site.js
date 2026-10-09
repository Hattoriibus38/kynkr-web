// Kynkr — site vitrine : menu mobile, apparition douce, formulaire « Me prévenir ».
(function () {
  'use strict';

  var FONCTION = 'https://byhudkuzmmngnnfiqpii.supabase.co/functions/v1/waitlist-signup';

  // Menu mobile (clavier : Entrée/Espace sur le bouton, Échap pour fermer et rendre le focus au bouton)
  var toggle = document.querySelector('.nav-toggle');
  var liens = document.querySelector('.nav-links');
  function fermerMenu(rendreFocus) {
    if (!toggle || !liens || !liens.classList.contains('open')) return;
    liens.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Ouvrir le menu');
    if (rendreFocus) toggle.focus();
  }
  if (toggle && liens) {
    toggle.addEventListener('click', function () {
      var ouvert = liens.classList.toggle('open');
      toggle.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
      toggle.setAttribute('aria-label', ouvert ? 'Fermer le menu' : 'Ouvrir le menu');
    });
    liens.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') fermerMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') fermerMenu(true);
    });
    // Retour arrière (page restaurée du cache) ou passage en grand écran : le menu ne reste pas ouvert
    window.addEventListener('pageshow', function () { fermerMenu(false); });
    window.addEventListener('resize', function () { if (window.innerWidth > 900) fermerMenu(false); });
  }

  // Apparition douce au défilement.
  // Le contenu est visible par défaut : la classe « js » (posée ici) n'active l'effet que si tout fonctionne.
  // Ce qui est déjà à l'écran ou déjà dépassé (retour arrière, défilement restauré par le navigateur, ancre #…)
  // est montré immédiatement, sans attendre l'IntersectionObserver (il ne se déclenche pas toujours après une
  // restauration de défilement, ni dans un onglet masqué).
  var elements = [].slice.call(document.querySelectorAll('.reveal'));
  var mouvementReduit = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var restants = elements.slice();

  function atteint(el) {
    var hauteur = window.innerHeight || document.documentElement.clientHeight;
    return el.getBoundingClientRect().top < hauteur * 0.95;
  }
  function revelerAtteints() {
    restants = restants.filter(function (el) {
      if (atteint(el)) { el.classList.add('in'); return false; }
      return true;
    });
    if (!restants.length) {
      window.removeEventListener('scroll', surDefilement);
      window.removeEventListener('resize', revelerAtteints);
    }
  }
  var attente = false;
  function surDefilement() {
    if (attente) return;
    attente = true;
    window.requestAnimationFrame(function () { attente = false; revelerAtteints(); });
  }

  if (elements.length && !mouvementReduit) {
    revelerAtteints();                       // avant la classe « js » : rien ne clignote
    document.documentElement.classList.add('js');
    if (restants.length) {
      if ('IntersectionObserver' in window) {
        var obs = new IntersectionObserver(function (entrees) {
          entrees.forEach(function (en) {
            if (en.isIntersecting) { en.target.classList.add('in'); obs.unobserve(en.target); }
          });
        }, { threshold: 0.12 });
        restants.forEach(function (el) { obs.observe(el); });
      }
      // Filet de sécurité : défilement, redimensionnement, retour de page (cache arrière-avant), retour d'onglet
      window.addEventListener('scroll', surDefilement, { passive: true });
      window.addEventListener('resize', revelerAtteints);
      window.addEventListener('pageshow', revelerAtteints);
      window.addEventListener('load', revelerAtteints);
      window.addEventListener('hashchange', revelerAtteints);
      document.addEventListener('visibilitychange', function () { if (!document.hidden) revelerAtteints(); });
      setTimeout(revelerAtteints, 600);
    }
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
