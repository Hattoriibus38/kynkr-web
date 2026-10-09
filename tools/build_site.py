# Générateur du site Kynkr : produit les pages HTML à partir de gabarits communs (en-tête, navigation, pied de page).
# Usage : python tools/build_site.py   (depuis la racine du dépôt kynkr-web)
import os
import re
import html
import hashlib

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://www.kynkr.app'
MAJ = '9 octobre 2026'


def version_asset(chemin):
    """Empreinte courte d'un fichier de assets/ : change à chaque modification, ce qui contourne le cache de 7 jours
    (Cache-Control sur /assets/) pour que les visiteurs reçoivent tout de suite le CSS et le JS corrigés."""
    with open(os.path.join(RACINE, 'assets', chemin), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

# ─────────────────────────── Éléments communs ───────────────────────────

def icone(nom):
    """Icônes à trait fin (24×24), même esprit que les Ionicons de l'app."""
    chemins = {
        'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
        'trophee': '<path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4zM17 5h3v2a3 3 0 0 1-3 3M7 5H4v2a3 3 0 0 0 3 3"/>',
        'livre': '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5v-16zM4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>',
        'courbe': '<path d="M3 17l5-5 4 4 8-9"/><path d="M15 7h5v5"/>',
        'groupe': '<circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9.5" r="2.4"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5M15.5 14.8c2.8-.4 5.5 1.3 5.5 4.2"/>',
        'boussole': '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
        'cadenas': '<rect x="5" y="11" width="14" height="10" rx="2.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
        'calculatrice': '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8.5 7h7M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01"/>',
        'secousse': '<path d="M9 5l-4 3 4 3M15 13l4 3-4 3M5 8h9a4 4 0 0 1 0 8M19 16H10"/>',
        'oeil-barre': '<path d="M3 3l18 18M10.6 6.2A9.8 9.8 0 0 1 12 6c5 0 8.5 4.2 9.5 6-.4.8-1.4 2.2-2.9 3.5M6.3 7.7C4.4 9 3.2 10.8 2.5 12c1 1.8 4.5 6 9.5 6 1.6 0 3-.4 4.2-1M9.9 9.9a3 3 0 0 0 4.2 4.2"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    }
    return ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>' % chemins[nom])


NAV = [('/#fonctionnalites', 'Fonctionnalités', None), ('/#discretion', 'Discrétion', None),
       ('/premium', 'Premium', 'premium'), ('/contact', 'Contact', 'contact')]


def nav(courant=None):
    liens = ''.join(
        '<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if cle and cle == courant else '', t)
        for h, t, cle in NAV)
    return f'''<a class="skip-link" href="#contenu">Aller au contenu</a>
<div class="halo-bg" aria-hidden="true"></div>
<header class="site-nav">
  <a href="/" class="logo" aria-label="Kynkr, accueil">Kynk<span>r</span></a>
  <ul class="nav-links" id="menu">{liens}</ul>
  <div class="nav-right">
    <a href="/#prevenir" class="btn btn-sm">Me prévenir</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu">{icone('menu')}</button>
  </div>
</header>'''


def pied():
    return f'''<footer class="site-footer">
  <div class="footer-grid">
    <div>
      <a href="/" class="logo" aria-label="Kynkr, accueil">Kynk<span>r</span></a>
      <p class="footer-about">L'application des couples qui prennent soin de leur relation. Réservée aux personnes majeures.</p>
    </div>
    <div><h4>Produit</h4><ul><li><a href="/#fonctionnalites">Fonctionnalités</a></li><li><a href="/#discretion">Discrétion</a></li><li><a href="/premium">Premium</a></li></ul></div>
    <div><h4>Légal</h4><ul><li><a href="/privacy">Confidentialité</a></li><li><a href="/cgu">Conditions d'utilisation</a></li><li><a href="/suppression-compte">Supprimer mon compte</a></li></ul></div>
    <div><h4>Contact</h4><ul><li><a href="mailto:contact@kynkr.app">contact@kynkr.app</a></li><li><a href="/contact">Nous écrire</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>© 2026 Kynkr — Tous droits réservés</span><span>Kynkr est réservé aux adultes (18 ans et plus).</span></div>
</footer>
<script src="/assets/site.js?v={version_asset('site.js')}" defer></script>
<script defer src="/_vercel/insights/script.js"></script>'''


def tete(titre, description, chemin, og_titre=None, noindex=False):
    t = html.escape(titre)
    d = html.escape(description)
    ot = html.escape(og_titre or titre)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ''
    canonique = '' if noindex else f'<link rel="canonical" href="{URL}{chemin}">\n'
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
{robots}<meta name="theme-color" content="#1a0f1e">
{canonique}<meta property="og:type" content="website">
<meta property="og:site_name" content="Kynkr">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{ot}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{URL}{chemin}">
<meta property="og:image" content="{URL}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Manrope:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={version_asset('site.css')}">
</head>
<body>'''


def page(titre, description, chemin, corps, courant=None, **kw):
    return tete(titre, description, chemin, **kw) + '\n' + nav(courant) + '\n' + corps + '\n' + pied() + '\n</body>\n</html>\n'


def telephone(img, alt, classe='', lazy=True):
    chargement = ' loading="lazy"' if lazy else ''
    return (f'<div class="phone {classe}"><div class="phone-screen">'
            f'<img src="/assets/app/{img}.webp" width="540" height="1200" alt="{html.escape(alt)}"{chargement} decoding="async"></div></div>')


def formulaire_attente(source='site', centre=False):
    cls = 'waitlist centre' if centre else 'waitlist'
    return f'''<form class="{cls}" data-source="{source}" novalidate>
  <label class="sr-only" for="email-{source}">Ton adresse email</label>
  <input class="waitlist-input" id="email-{source}" name="email" type="email" inputmode="email" autocomplete="email" placeholder="Ton adresse email" required>
  <input class="waitlist-trap" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  <button class="btn" type="submit">Me prévenir</button>
</form>
<p class="waitlist-status" role="status" aria-live="polite"></p>'''


NOTE_ATTENTE = ('<p class="waitlist-note">En t\'inscrivant, tu acceptes que ton adresse serve uniquement à t\'avertir de l\'ouverture. '
                '<a href="/privacy#liste-attente">En savoir plus</a>.</p>')

# ─────────────────────────── Accueil ───────────────────────────

CARTES = [
    ('chat', '', 'Messagerie du couple', 'Un espace de discussion privé, rien qu\'à vous deux : GIF, réactions, messages épinglés, souvenirs partagés.'),
    ('trophee', 'sec', 'Défi du jour', 'Chaque jour, un défi à relever ensemble. Rituels, jeux, moments complices pour ne jamais tomber dans la routine.'),
    ('livre', 'sec', 'Carnet & capsules', 'Garde vos souvenirs dans un carnet partagé, et glisse des messages dans une capsule temporelle à ouvrir plus tard.'),
    ('courbe', '', 'Quiz de compatibilité', 'Explore ce qui vous unit et ce qui vous distingue : des questions pour mieux te connaître, et mieux vous connaître.'),
    ('groupe', '', 'Espaces communautaires', 'Rejoins des espaces privés avec d\'autres couples pour partager, t\'inspirer, et ne pas naviguer seul.'),
    ('boussole', '', 'Découverte de profils', 'Rencontre d\'autres couples qui te ressemblent. Échange, connecte-toi, élargis ton cercle à ton rythme.'),
]

POINTS = [
    ('cadenas', '', 'Un verrou à toi', 'Un code PIN ou ta biométrie pour entrer dans l\'app. Personne d\'autre que toi n\'ouvre la porte.'),
    ('calculatrice', 'sec', 'Un mode discret', 'L\'app peut se déguiser en calculatrice qui fonctionne vraiment. Rien ne laisse deviner ce qu\'elle cache.'),
    ('secousse', '', 'Un geste, et tout se range', 'Secoue ton téléphone : un écran neutre prend aussitôt la place. Tu reviens quand tu veux, avec ton code.'),
    ('oeil-barre', 'sec', 'Captures d\'écran bloquées', 'Elles sont bloquées par défaut. Tu choisis si tu les autorises, jamais l\'inverse.'),
]


def accueil():
    cartes = ''.join(
        f'<article class="card reveal"><div class="icon-box {c}">{icone(i)}</div><h3>{t}</h3><p>{d}</p></article>'
        for i, c, t, d in CARTES)
    points = ''.join(
        f'<li class="card reveal"><div class="icon-box {c}">{icone(i)}</div><h3>{t}</h3><p>{d}</p></li>'
        for i, c, t, d in POINTS)
    ecrans = [
        ('defi', 'Le défi du jour dans Kynkr', 'Un défi à relever chaque jour. Ensemble.'),
        ('carnet', 'Un souvenir dans le carnet de Kynkr', 'Tes souvenirs, toujours là quand tu en as besoin.'),
        ('espaces', 'La liste des espaces communautaires', 'Des espaces privés avec d\'autres couples.'),
        ('chat', 'La discussion d\'un espace', 'Des échanges vrais, dans un cadre bienveillant.'),
    ]
    galerie = ''.join(
        f'<figure class="screen-item reveal">{telephone(i, a, "s")}<figcaption>{c}</figcaption></figure>' for i, a, c in ecrans)
    alt_accueil = "L'écran d'accueil de Kynkr : 427 jours ensemble, humeurs du jour et défi du jour"
    tel_accueil = telephone('accueil', alt_accueil, 'p1', lazy=False)
    tel_messagerie = telephone('messagerie', 'La messagerie du couple dans Kynkr', 'p2', lazy=False)
    tel_avant = telephone('sondage-avant', 'Un sondage avant le vote', 's')
    tel_apres = telephone('sondage-apres', 'Le même sondage après le vote, avec les résultats', 's')
    corps = f'''<main id="contenu">
<section class="hero" id="prevenir">
  <div class="hero-text">
    <span class="chip">Ouverture prochaine</span>
    <h1 class="hero-title">Ta vie à deux, un espace <em>rien qu'à vous</em>.</h1>
    <p class="hero-sub">Kynkr réunit tout ce dont tu as besoin pour nourrir ta relation : souvenirs, défis, jeux, espaces entre couples. Au quotidien comme dans les moments qui comptent.</p>
    {formulaire_attente('site')}
    {NOTE_ATTENTE}
    <a href="#fonctionnalites" class="btn btn-ghost">Voir les fonctionnalités →</a>
  </div>
  <div class="hero-phones" aria-hidden="false">
    {tel_accueil}
    {tel_messagerie}
  </div>
</section>

<section class="section wrap" id="fonctionnalites">
  <p class="eyebrow">Ce que tu trouveras</p>
  <h2 class="h2">Tout ce dont un couple a besoin</h2>
  <p class="lead">Un seul endroit pour partager, planifier, découvrir et vous retrouver, avec les personnes qui comptent vraiment.</p>
  <div class="divider"></div>
  <div class="grid-3">{cartes}</div>
</section>

<section class="section band" aria-labelledby="dans-lapp">
  <div class="wrap">
    <p class="eyebrow">Dans l'app</p>
    <h2 class="h2" id="dans-lapp">Vois avant d'essayer</h2>
    <p class="lead">Quatre écrans, quatre façons de nourrir ta relation au quotidien.</p>
    <div class="divider"></div>
    <div class="screens">{galerie}</div>
    <div class="poll-block reveal">
      <div>
        <p class="eyebrow left">Ta voix compte</p>
        <h3 class="poll-title">Tu guides ce qu'on construit.</h3>
        <p class="poll-desc">Des sondages réguliers pour que chacun puisse orienter les prochaines fonctionnalités. Tu choisis de rester anonyme ou non, et tu peux changer d'avis quand tu veux.</p>
      </div>
      <div class="poll-phones">
        <figure>{tel_avant}<figcaption>Avant</figcaption></figure>
        <figure>{tel_apres}<figcaption>Après</figcaption></figure>
      </div>
    </div>
  </div>
</section>

<section class="section wrap" id="discretion">
  <p class="eyebrow">Discrétion</p>
  <h2 class="h2">Ton intimité t'appartient</h2>
  <p class="lead">Kynkr est pensé pour qu'on s'y sente en sécurité, même quand quelqu'un regarde par-dessus ton épaule.</p>
  <div class="divider"></div>
  <ul class="points">{points}</ul>
</section>

<section class="section band">
  <div class="wrap">
    <p class="eyebrow">Gratuit pour commencer</p>
    <h2 class="h2">Va plus loin quand tu le souhaites</h2>
    <p class="lead">L'essentiel de Kynkr est gratuit. Premium, l'offre Couple et le VIP à vie débloquent plus d'espace, plus d'options et un accès anticipé aux nouveautés.</p>
    <p class="lead"><a class="btn" href="/premium">Découvrir les offres</a></p>
  </div>
</section>

<section class="section wrap" aria-labelledby="cta-final">
  <div class="poll-block reveal">
    <div>
      <p class="eyebrow left">Bientôt</p>
      <h2 class="poll-title" id="cta-final">Sois prévenu·e dès l'ouverture.</h2>
      <p class="poll-desc">Laisse ton adresse : on t'écrit une seule fois, quand Kynkr ouvre ses portes.</p>
    </div>
    <div>
      {formulaire_attente('contact')}
      {NOTE_ATTENTE}
    </div>
  </div>
</section>
</main>'''
    return page('Kynkr — Ta vie à deux, un espace rien qu\'à vous',
                'Kynkr réunit souvenirs, défis, jeux et espaces entre couples. Messagerie privée, carnet partagé, sondages, mode discret. Ouverture prochaine.',
                '/', corps)


# ─────────────────────────── Premium ───────────────────────────

OFFRES = [
    dict(nom='Gratuit', tag='Pour commencer l\'aventure', prix='0 €', alt='Pour toujours',
         liste=['Profil complet et messagerie du couple', 'Défi du jour et carnet de souvenirs', 'Quiz de compatibilité',
                'Jusqu\'à 5 espaces communautaires', 'Découverte de profils et sondages', 'Verrou PIN, mode discret et écran neutre'], vedette=False, badge=None),
    dict(nom='Premium', tag='Plus d\'espace, plus d\'options', prix='9,99 €', unite='/ mois', alt='ou 59,99 € par an, soit −50 %',
         liste=['Tout le Gratuit', 'Galerie jusqu\'à 200 photos, 50 souhaits, 20 capsules', 'Jusqu\'à 20 espaces rejoints, 500 membres par espace créé',
                'Vidéos éphémères et messages vocaux', 'Voir qui t\'a liké, boost de profil', 'Thèmes premium'], vedette=False, badge=None),
    dict(nom='Premium Couple', tag='Un seul abonnement pour vous deux', prix='14,99 €', unite='/ mois', alt='ou 89,99 € par an, soit −50 %',
         liste=['Tout Premium, pour toi et ton partenaire', 'Un seul abonnement, deux comptes liés', 'La couverture s\'arrête si le couple se sépare',
                'Idéal pour profiter de tout, ensemble'], vedette=True, badge='Le plus choisi'),
    dict(nom='VIP à vie', tag='Un paiement, pour toujours', prix='249 €', unite='une fois', alt='Sans abonnement ni renouvellement',
         liste=['Tout Premium, avec les limites les plus hautes', 'Le Labo : accès anticipé aux nouveautés', 'Sondages privilégiés avec les bêta testeurs',
                'Badge Fondateur numéroté pour les premiers', 'Thème de couleurs personnalisable', 'Support prioritaire'], vedette=False, badge=None),
]


def premium():
    cartes = ''
    for o in OFFRES:
        prix = f'<div class="price">{o["prix"]} <small>{o.get("unite", "")}</small></div>'
        badge = f'<span class="badge-top">{o["badge"]}</span>' if o['badge'] else ''
        lis = ''.join(f'<li>{html.escape(x)}</li>' for x in o['liste'])
        cartes += (f'<article class="tier reveal{" featured" if o["vedette"] else ""}">{badge}<h3>{o["nom"]}</h3>'
                   f'<p class="tag">{o["tag"]}</p>{prix}<p class="price-alt">{o["alt"]}</p><ul>{lis}</ul></article>')
    corps = f'''<main id="contenu">
<section class="section wrap top-offset">
  <p class="eyebrow">Les offres</p>
  <h1 class="h2">Va plus loin, à ton rythme</h1>
  <p class="lead">Kynkr est gratuit pour commencer. Choisis une offre seulement si tu veux plus de place, plus d'options et plus de nouveautés.</p>
  <div class="divider"></div>
  <div class="tiers">{cartes}</div>
  <p class="fine">Les abonnements se souscrivent dans l'application, via l'App Store ou Google Play, et s'annulent à tout moment depuis ton compte du store.
  Les annuels profitent de 7 jours d'essai, avec un rappel avant le premier prélèvement. Tarifs de lancement, susceptibles d'évoluer avant l'ouverture.</p>
  <div class="divider mt"></div>
  <p class="lead">Les offres ouvrent avec l'application.</p>
  <div class="centre-bloc">{formulaire_attente('premium', centre=True)}{NOTE_ATTENTE}</div>
</section>
</main>'''
    return page('Les offres Kynkr — Gratuit, Premium, Couple et VIP à vie',
                'Découvre les offres Kynkr : gratuit pour commencer, Premium, offre Couple pour deux comptes liés et VIP à vie.',
                '/premium', corps, courant='premium')


# ─────────────────────────── Contact, suppression, CGU, 404 ───────────────────────────

def contact():
    corps = f'''<main id="contenu" class="legal">
  <div class="page-header">
    <div class="badge">Contact</div>
    <h1>Nous écrire</h1>
    <div class="accent-bar"></div>
    <p class="meta">Une question, un retour, un souci ? On lit tout.</p>
  </div>
  <div class="contact-grid">
    <article class="card"><h3>Question générale</h3><p>Sur l'app, les offres, la bêta.</p><p><a href="mailto:contact@kynkr.app?subject=Question%20sur%20Kynkr">contact@kynkr.app</a></p></article>
    <article class="card"><h3>Un problème technique</h3><p>Indique ton téléphone, la version de l'app et ce qui s'est passé.</p><p><a href="mailto:contact@kynkr.app?subject=Probl%C3%A8me%20technique">contact@kynkr.app</a></p></article>
    <article class="card"><h3>Tes données</h3><p>Accès, rectification, suppression : voir <a href="/privacy">la confidentialité</a> ou <a href="/suppression-compte">la suppression de compte</a>.</p><p><a href="mailto:contact@kynkr.app?subject=Mes%20donn%C3%A9es">contact@kynkr.app</a></p></article>
  </div>
  <p class="fine mt">Kynkr est édité par un développeur indépendant basé en France. Nous répondons en général sous quelques jours.</p>
</main>'''
    return page('Contact — Kynkr', 'Contacter l\'équipe Kynkr : questions, retours, support technique et demandes relatives à tes données.',
                '/contact', corps, courant='contact')


def suppression():
    corps = '''<main id="contenu" class="legal">
  <div class="page-header">
    <div class="badge">Tes données</div>
    <h1>Supprimer mon compte</h1>
    <div class="accent-bar"></div>
    <p class="meta">Dernière mise à jour : ''' + MAJ + '''</p>
  </div>
  <div class="intro-card"><strong>En bref :</strong> tu peux supprimer ton compte et tes données à tout moment, directement depuis l'application. Un délai de réflexion de 30 jours est appliqué avant l'effacement définitif.</div>
  <div class="section">
    <h2>Depuis l'application</h2>
    <div class="section-divider"></div>
    <ul>
      <li>Ouvre Kynkr, puis l'onglet <strong>Profil</strong>.</li>
      <li>Va dans <strong>Sécurité</strong>.</li>
      <li>Choisis <strong>Supprimer mon compte</strong> et confirme.</li>
    </ul>
    <p>Pendant 30 jours, tu peux te reconnecter pour annuler la demande. Passé ce délai, ton compte et tes données personnelles sont effacés (voir les durées de conservation dans la <a href="/privacy">politique de confidentialité</a>).</p>
  </div>
  <div class="section">
    <h2>Par e-mail</h2>
    <div class="section-divider"></div>
    <p>Si tu ne peux plus accéder à l'application, écris-nous depuis l'adresse e-mail de ton compte à <a href="mailto:contact@kynkr.app?subject=Suppression%20de%20compte">contact@kynkr.app</a> avec l'objet « Suppression de compte ». Nous te répondons pour confirmer la demande.</p>
  </div>
  <div class="section">
    <h2>Liste d'attente du site</h2>
    <div class="section-divider"></div>
    <p>Pour retirer ton adresse de la liste d'attente, écris-nous à <a href="mailto:contact@kynkr.app?subject=Retrait%20liste%20d%27attente">contact@kynkr.app</a> : elle sera supprimée sans délai.</p>
  </div>
  <div class="section">
    <h2>Ton abonnement</h2>
    <div class="section-divider"></div>
    <p>Supprimer ton compte n'annule pas automatiquement un abonnement pris via l'App Store ou Google Play. Pense à le résilier depuis ton compte du store.</p>
  </div>
</main>'''
    return page('Supprimer mon compte — Kynkr', 'Comment supprimer ton compte Kynkr et tes données : depuis l\'application ou par e-mail.',
                '/suppression-compte', corps)


def cgu():
    corps = '''<main id="contenu" class="legal">
  <div class="page-header">
    <div class="badge">Légal</div>
    <h1>Conditions générales<br>d'utilisation</h1>
    <div class="accent-bar"></div>
    <p class="meta">Dernière mise à jour : ''' + MAJ + ''' · Version de la bêta</p>
  </div>
  <div class="intro-card"><strong>En résumé :</strong> Kynkr est réservé aux adultes. On y prend soin de sa relation et on y rencontre des personnes dans le respect du consentement, de la vie privée et de chacun. Les abus sont modérés et peuvent mener à une exclusion.</div>

  <div class="section"><h2>1. Objet</h2><div class="section-divider"></div>
    <p>Les présentes conditions encadrent l'utilisation de l'application mobile Kynkr et du site kynkr.app (le « Service »), édités par Kylian Vuillemin, développeur indépendant basé en France (contact : <a href="mailto:contact@kynkr.app">contact@kynkr.app</a>). En créant un compte, tu les acceptes.</p></div>

  <div class="section"><h2>2. Accès au Service</h2><div class="section-divider"></div>
    <ul>
      <li>Le Service est <strong>strictement réservé aux personnes âgées de 18 ans révolus</strong>. Une vérification de l'âge peut être demandée.</li>
      <li>Tu fournis des informations exactes et tu es responsable de la confidentialité de tes identifiants et de ton code PIN.</li>
      <li>Un compte est personnel. Il ne peut être ni cédé ni partagé.</li>
      <li>Pendant la bêta, l'accès peut être limité, interrompu ou modifié sans préavis, et des fonctionnalités peuvent évoluer.</li>
    </ul></div>

  <div class="section"><h2>3. Comportement attendu</h2><div class="section-divider"></div>
    <p>Kynkr repose sur le consentement et le respect. Sont notamment interdits :</p>
    <ul>
      <li>tout contenu ou comportement impliquant des mineurs ;</li>
      <li>le harcèlement, les menaces, les propos haineux ou discriminatoires ;</li>
      <li>le partage de photos, vidéos ou messages intimes d'une personne sans son accord ;</li>
      <li>l'usurpation d'identité, les faux profils, la sollicitation commerciale ou frauduleuse ;</li>
      <li>tout contenu illégal, ainsi que toute activité de prostitution ou de traite d'êtres humains ;</li>
      <li>le contournement des mesures de sécurité ou de modération du Service.</li>
    </ul>
    <p>Les surfaces publiques de Kynkr n'acceptent aucun contenu explicite. Les échanges privés restent sous la responsabilité de leurs auteurs et de leurs destinataires.</p></div>

  <div class="section"><h2>4. Contenus et modération</h2><div class="section-divider"></div>
    <p>Tu conserves tes droits sur les contenus que tu publies et tu nous accordes la licence nécessaire pour les héberger et les afficher dans le Service. Tu peux signaler un contenu ou un profil depuis l'application. Selon la gravité, nous pouvons retirer un contenu, mettre un compte en sourdine, le suspendre ou le supprimer définitivement. Un compte exclu ne peut pas se réinscrire.</p></div>

  <div class="section"><h2>5. Offres et abonnements</h2><div class="section-divider"></div>
    <ul>
      <li>Le Service propose une offre gratuite et des offres payantes : <strong>Premium</strong>, <strong>Premium Couple</strong> (un abonnement couvrant deux comptes liés) et <strong>VIP à vie</strong>.</li>
      <li>Les achats se font via l'App Store ou Google Play et sont soumis à leurs conditions. L'abonnement se renouvelle automatiquement jusqu'à sa résiliation depuis ton compte du store, au moins 24 h avant l'échéance.</li>
      <li>Pour Premium Couple, la couverture du partenaire cesse si le couple est délié ou si l'abonnement prend fin.</li>
      <li>Le <strong>VIP à vie</strong> est un paiement unique valable pour la durée d'exploitation du Service. Il donne accès à toutes les fonctionnalités de l'application, présentes et futures, à l'exception de services dont le coût externe est significatif, qui pourront faire l'objet d'une offre distincte.</li>
      <li>Les remboursements sont gérés par le store concerné. Tu peux demander à renoncer à ton droit de rétractation pour le contenu numérique fourni immédiatement ; les périodes d'essai sont décrites dans l'application.</li>
    </ul></div>

  <div class="section"><h2>6. Données personnelles</h2><div class="section-divider"></div>
    <p>Le traitement de tes données est décrit dans notre <a href="/privacy">politique de confidentialité</a>. Certaines données relèvent de la vie intime : elles ne sont traitées qu'avec ton consentement explicite, que tu peux retirer à tout moment.</p></div>

  <div class="section"><h2>7. Disponibilité et responsabilité</h2><div class="section-divider"></div>
    <p>Nous faisons de notre mieux pour assurer un Service fiable, mais il est fourni « en l'état », sans garantie d'absence d'interruption ou d'erreur, en particulier pendant la bêta. Kynkr n'est pas responsable des rencontres ou échanges entre utilisateurs : sois vigilant·e et protège tes informations personnelles. Notre responsabilité est limitée aux dommages directs et prévisibles, dans la mesure permise par la loi.</p></div>

  <div class="section"><h2>8. Propriété intellectuelle</h2><div class="section-divider"></div>
    <p>La marque Kynkr, le logo, l'interface, les textes et les illustrations sont protégés. Toute reproduction ou réutilisation sans autorisation écrite est interdite.</p></div>

  <div class="section"><h2>9. Résiliation</h2><div class="section-divider"></div>
    <p>Tu peux supprimer ton compte à tout moment (voir <a href="/suppression-compte">Supprimer mon compte</a>). Nous pouvons suspendre ou supprimer un compte qui enfreint ces conditions.</p></div>

  <div class="section"><h2>10. Modifications</h2><div class="section-divider"></div>
    <p>Ces conditions peuvent évoluer. En cas de changement important, nous t'en informons dans l'application. Continuer à utiliser le Service après notification vaut acceptation.</p></div>

  <div class="section"><h2>11. Droit applicable et litiges</h2><div class="section-divider"></div>
    <p>Les présentes conditions sont soumises au droit français. En cas de litige, une solution amiable est recherchée en priorité ; tu peux aussi recourir gratuitement à un médiateur de la consommation. À défaut, les tribunaux français sont compétents, sans préjudice de tes droits de consommateur.</p></div>

  <div class="contact-card"><strong>Une question sur ces conditions ?</strong><br>Écris-nous à <a href="mailto:contact@kynkr.app">contact@kynkr.app</a>.</div>
</main>'''
    return page('Conditions générales d\'utilisation — Kynkr', 'Les conditions d\'utilisation de Kynkr : accès réservé aux adultes, comportement attendu, offres et abonnements, données et modération.',
                '/cgu', corps)


def non_trouvee():
    corps = '''<main id="contenu" class="legal">
  <div class="page-header">
    <div class="badge">404</div>
    <h1>Cette page s'est éclipsée</h1>
    <div class="accent-bar"></div>
    <p class="meta">Le lien est peut-être périmé. Retourne à l'essentiel.</p>
  </div>
  <p class="centre"><a class="btn" href="/">Retour à l'accueil</a></p>
</main>'''
    return page('Page introuvable — Kynkr', 'Cette page n\'existe pas ou n\'existe plus.', '/404', corps, noindex=True)


# ─────────────────────────── Confidentialité (reprise du texte existant) ───────────────────────────

def confidentialite():
    src = os.path.join(RACINE, '_sources', 'privacy_corps.html')
    with open(src, encoding='utf-8') as f:
        c = f.read()
    # Nouvelles sections : liste d'attente et sondages
    liste_attente = '''<div class="section" id="liste-attente">
      <h2>Liste d'attente du site</h2>
      <div class="section-divider"></div>
      <p>Si tu laisses ton adresse e-mail sur kynkr.app pour être prévenu·e de l'ouverture, elle est enregistrée avec la date d'inscription et une empreinte non réversible de ton adresse IP (utilisée uniquement pour limiter les abus). Elle sert exclusivement à t'avertir de l'ouverture de l'application. Base légale : ton consentement. Elle est supprimée à l'ouverture si tu ne crées pas de compte, ou sur simple demande à <a href="mailto:contact@kynkr.app">contact@kynkr.app</a>.</p>
    </div>

    <div class="section" id="audience">
      <h2>Mesure d'audience du site</h2>
      <div class="section-divider"></div>
      <p>Le site kynkr.app utilise Vercel Web Analytics pour compter les visites (pages vues, pays, type d'appareil). Cet outil n'utilise <strong>aucun cookie</strong>, ne dépose rien sur ton appareil et ne te suit pas d'un site à l'autre : aucune donnée personnelle n'est conservée. Base légale : intérêt légitime à connaître la fréquentation du site.</p>
    </div>

    <div class="section" id="sondages">
      <h2>Sondages dans l'application</h2>
      <div class="section-divider"></div>
      <p>Tu peux répondre à des sondages destinés à orienter l'évolution de Kynkr. Pour établir des statistiques, ton sexe et ta tranche d'âge (jamais ta date de naissance) sont associés à ta réponse. Les groupes de moins de 5 personnes ne sont jamais affichés à l'équipe.</p>
      <p>Par défaut, ta réponse est <strong>anonyme</strong> : l'équipe ne voit que des chiffres. Si tu décoches « Rester anonyme », ton pseudo devient visible de l'équipe, qui peut te recontacter pour un retour détaillé. Tu peux changer ce choix, ou ta réponse, à tout moment. Si tu supprimes ton compte, le lien avec ton identité est effacé et seules des statistiques non identifiantes subsistent.</p>
    </div>
'''
    c = c.replace('<!-- 6. Vos droits -->', liste_attente + '\n    <!-- 6. Vos droits -->', 1)
    # Sous-traitants : hébergement du site et e-mails
    c = c.replace('''          <tr>
            <td>Stripe</td>''', '''          <tr>
            <td>Vercel</td>
            <td>Hébergement du site kynkr.app et mesure d'audience sans cookie</td>
            <td>USA / UE</td>
          </tr>
          <tr>
            <td>Resend</td>
            <td>Envoi des e-mails de support</td>
            <td>USA</td>
          </tr>
          <tr>
            <td>Stripe</td>''', 1)
    # Durées de conservation : liste d'attente et sondages
    c = c.replace('''          <tr>
            <td>Hash email banni''', '''          <tr>
            <td>Adresse e-mail de la liste d'attente</td>
            <td>Jusqu'à l'ouverture de l'application, ou sur simple demande</td>
          </tr>
          <tr>
            <td>Réponses aux sondages</td>
            <td>Le temps de l'analyse ; identité effacée à la suppression du compte</td>
          </tr>
          <tr>
            <td>Hash email banni''', 1)
    # Renumérote les titres 1…N
    compteur = {'n': 0}

    def renum(m):
        compteur['n'] += 1
        titre = re.sub(r'^\d+\.\s*', '', m.group(1))
        return '<h2>%d. %s</h2>' % (compteur['n'], titre)
    c = re.sub(r'<h2>(.*?)</h2>', renum, c)
    corps = f'''<main id="contenu" class="legal">
  <div class="page-header">
    <div class="badge">Légal</div>
    <h1>Politique de<br>confidentialité</h1>
    <div class="accent-bar"></div>
    <p class="meta">Dernière mise à jour : {MAJ}</p>
  </div>
  {c}
</main>'''
    return page('Politique de confidentialité — Kynkr', 'Comment Kynkr traite tes données personnelles : données collectées, bases légales, sous-traitants, durées de conservation et tes droits.',
                '/privacy', corps)


def typographie(doc):
    """Typographie française : espaces insécables avant : ; ? ! et à l'intérieur des guillemets (texte seulement, jamais dans les balises)."""
    def texte(m):
        s = m.group(1)
        for a, b in ((' :', '&nbsp;:'), (' ;', '&nbsp;;'), (' ?', '&nbsp;?'), (' !', '&nbsp;!'), ('« ', '«&nbsp;'), (' »', '&nbsp;»')):
            s = s.replace(a, b)
        return '>' + s + '<'
    return re.sub(r'>([^<>]+)<', texte, doc)


def ecrire(nom, contenu):
    chemin = os.path.join(RACINE, nom)
    contenu = typographie(contenu)
    with open(chemin, 'w', encoding='utf-8', newline='\n') as f:
        f.write(contenu)
    print('écrit', nom, len(contenu) // 1024, 'Ko')


if __name__ == '__main__':
    ecrire('index.html', accueil())
    ecrire('premium.html', premium())
    ecrire('contact.html', contact())
    ecrire('suppression-compte.html', suppression())
    ecrire('cgu.html', cgu())
    ecrire('privacy.html', confidentialite())
    ecrire('404.html', non_trouvee())
