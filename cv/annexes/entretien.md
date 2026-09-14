# Préparation d'entretien

Trois parties : ce qu'on va te demander, ce que tu demandes, ce qui doit t'alerter.

## 1. Les dix questions probables, et l'ossature de réponse

Une réponse tient en trois temps : le principe, un fait vécu, la limite que tu connais. Le troisième temps est celui qui distingue un architecte senior d'un candidat qui récite.

**1. Comment prouvez-vous qu'aucun message ne manque ?**
Trois niveaux indépendants — populations, volumétrie, fidélité — plus une mesure qui ne dépend pas des sources : des canaris quotidiens par canal dont on vérifie l'arrivée dans l'archive. Limite à énoncer : un décompte de source est lui-même une déclaration ; c'est pourquoi je ne fonde jamais la complétude sur un seul comptage.

**2. Par quoi commencez-vous ?**
Par le dénominateur : le périmètre attendu, versionné par jour, reconstruit à partir du RH, de l'annuaire, des entitlements et de la liste supervisée. Sans lui, aucun taux de complétude n'est défendable. C'est aussi la partie la plus politique, parce qu'elle oblige à désigner un propriétaire de la liste.

**3. Comment gérez-vous les écarts ?**
Un écart est soit expliqué, soit une exception avec propriétaire, cause présumée, échéance et statut. Ce que je regarde n'est pas le nombre d'exceptions mais l'ancienneté du plus vieil écart inexpliqué : c'est le seul chiffre qu'un auditeur retient.

**4. Quelle est la difficulté principale avec Teams ?**
Que la conversation est vivante — éditions, suppressions, réactions — et que la pièce jointe n'est pas dans le message mais dans SharePoint. Un record Teams n'est pas auto-portant : sans capture de versions et résolution des pièces jointes, on archive un état, pas une conversation. Et le coût d'extraction est un sujet de dossier, pas d'ingénierie.

**5. Et avec Bloomberg ?**
Les entitlements. La captation suit le droit d'accès : un départ ou une mobilité peut retirer la source elle-même. D'où un contrôle dédié aux départs, qui vérifie que la captation a duré jusqu'à la désactivation et que la rétention survit au départ. IB et MSG sont deux flux à traiter séparément.

**6. Comment articulez-vous conservation réglementaire et RGPD ?**
La durée réglementaire fixe un plancher de conservation, le RGPD un plafond d'usage : la conciliation se fait sur la **finalité** et l'accès, pas sur la durée. En pratique : périmètre limité aux personnes et canaux réellement concernés, accès restreint et journalisé, information des personnes et des instances représentatives, et suppression effective à l'échéance — ce qui suppose que la politique de rétention soit outillée et pas seulement écrite.

**7. Comment concevez-vous un PoC qui serve à décider ?**
Étroit sur le périmètre, complet sur la chaîne, et livré avec six chiffres : couverture, complétude par canal, délai de restitution p95, part de contrôles automatisés produisant une exception traçable, coût par million de messages, dépendances bloquantes. Un PoC qui ne produit que des captures d'écran ne fait pas décider.

**8. Comment tenez-vous le lineage sans en faire une charge ?**
En le faisant produire par la chaîne au lieu de le saisir à la main, et en le datant. La question à laquelle il doit répondre est unique : « d'où vient ce chiffre », jusqu'au lot reçu, dans la version de règle qui s'appliquait ce jour-là.

**9. Comment travaillez-vous avec Compliance et Risk ?**
En transformant leurs exigences en contrôles nommés, chiffrés et outillés, dont ils sont propriétaires. Un contrôle sans propriétaire métier ne survit pas six mois. Et je leur donne les exercices de restitution à l'aveugle : c'est leur meilleur levier et mon meilleur test.

**10. Qu'est-ce qui fait échouer ces programmes ?**
Trois causes, dans l'ordre : commencer par la captation avant d'avoir un périmètre attendu ; tolérer des écarts non expliqués parce que le volume est grand ; et confondre archiver avec pouvoir restituer. Aucune n'est technique.

## 2. Les questions à poser — elles jaugent la maturité du programme

1. Qui **possède** la liste des personnes supervisées, et à quelle fréquence est-elle réconciliée avec le RH et les entitlements ?
2. Quelle est l'archive de référence, et sait-elle **acquitter** ce qu'elle reçoit — c'est-à-dire produire un décompte opposable ?
3. Quel délai de restitution est exigé, par qui, et a-t-il déjà été testé à l'aveugle ?
4. Quelles entités juridiques sont dans le périmètre, et donc quels régulateurs ? Y a-t-il des entités US ?
5. Quels canaux au-delà d'Exchange, Teams et Bloomberg : voix, mobile, messageries grand public ?
6. Quel outillage existe déjà en data quality, lineage et réconciliation, et qu'est-il interdit de redoubler ?
7. Le programme est-il né d'une remédiation (constat d'audit, revue régulateur) ou d'une refonte volontaire ? Cela change tout au calendrier et à la marge d'arbitrage.
8. Qui tranche quand l'exigence réglementaire et la faisabilité s'opposent — Compliance, Risk, ou la DSI ?
9. Quel est le périmètre du PoC déjà décidé en interne, et par qui ?
10. Qui portera le build : équipes internes, offshore, éditeur ? Quel est mon rôle réel sur ce build ?
11. Comment le succès du Lead Architect est-il mesuré à six mois ?
12. Quelle est la comitologie, en quelle langue, et avec quelles instances ?

## 3. Ce qui doit t'alerter

- **Personne ne possède la liste des personnes supervisées.** Le programme va passer six mois sur le dénominateur ; il faut l'annoncer au lieu de le découvrir.
- **L'archive n'acquitte pas.** Sans accusé opposable, le niveau 2 de réconciliation est bancal par construction ; il faut alors une mesure indépendante — canaris et hachage — et le dire tôt.
- **« Lead Architect » sans droit de décision.** Si l'architecture est déjà arrêtée par un éditeur et que le rôle consiste à la documenter, l'intitulé ne correspond pas au contenu.
- **PoC daté avant que le périmètre soit défini.** Signe que la date vient d'un engagement externe ; c'est jouable, mais alors le périmètre doit être réduit explicitement, par écrit.
- **Aucun accès aux équipes Operations.** Sans elles, pas de propriétaire d'exception, donc pas de contrôle vivant.

## 4. Les trois choses à faire avant l'entretien

1. **Combler les `[[trous]]` du CV** ([`../README.md`](../README.md)) : le CV doit être défendable ligne à ligne.
2. **Préparer deux récits chiffrés** : un rapprochement difficile, un contrôle manuel automatisé. Avec les chiffres avant/après. C'est ce qui se retient.
3. **Décider ta position sur l'anglais et sur la disponibilité** : ces deux points seront posés, et l'hésitation coûte plus cher que la réponse.
