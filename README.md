# Flask_ENT

squelette :
Flask 
  - DB sqli3 : ✅
    - user : ID nom prenom mail mdp role
    - note: ID TEXT creater_user(link au user qui la cree) user_concerner(lier au etudiant) devoir
    - devoir: ID user_id Contenu_du_devoir
    - cours: ID name creater_user user_concerner devoir

  - features principales : 
    - role (admin, prof, user)(CRUD) ❌
    - note(CRUD) ❌
    - planing(CRUD) ❌


  - features secondaire: 
    - messagerie (CRUD)❌ 
    - absent/retard (CRUD) ❌ 
