# EN
# Packet to extract and store various social network data in a common database


## Guide to get started:
**Step 1)** Download the complete project as a zip file (the green button on the top right).
**Step 2)** Unzip the zip file into an empty folder (the folder will host the project).
**Step 3)** Open the *".py "* files.
You are now ready to use the package.

## How to make a scraping :
### Phase 1 (Extraction in csv)
#### (The goal is to first accumulate the data from the social networks in csv files).
**Step 1)** Open the file *"superfunction.py "*.
**Step 2)** Write your query by constructing it like this:
*scrapeMediaPostBySearch("vaccinated", count=50, post_file="vaccin_table_post.csv", profile_file="vaccin_table_profile.csv")*
- The first argument is the keyword that will be searched, here it is the word "vaccinated".
- The second argument is the maximum number of posts that will be searched (per social network).
- The third argument is the name of the CSV file that will be created to store the posts.
- The fourth argument is the name of the CSV file that will be created to store the profiles.

**Step 3)** Repeat step 2 with a different keyword to accumulate the data in the same csv files.

### Step 2 (Prepare the SQLite database)
#### (To be able to store the data, it is necessary to have a ready SQLite database).
**Step 1)** Copy the empty SQLite database template named *"sqlite_template.db "*.
**Step 2)** Rename the file to your liking, example : *"vaccine_sqlite.db "*.

### Step 3 (Store in SQLite)
#### (Now that the csv files are created, we need to inject the csv files into a SQLite database).
**Step 1)** Open the file *"csv_to_sql.py "*.
**Step 2)** Write your query by building it this way:
for profiles: *csvToSqlite("vaccin_table_profile", "vaccin_db", "table_profile", profile_structure)*
for positions: *csvToSqlite("vaccin_table_post", "vaccin_db", "table_post", post_structure)*
- The first argument is the name of the csv file that will be transferred (the name without the *".csv "*).
- The second argument is the name of the destination SQLite database.
- The third argument is the name of the destination table within the SQLite database (there are two : *"table_profile "* for profiles and *"table_post "* for posts).
- The fourth argument corresponds to the data structure of the csv file and the table (there are two of them: *"profile_structure "* for profiles and *"post_structure "* for posts).

**Step 3)** To delete a table in the SQLite database, use the function : *resetTable("vaccine_db", "table_profile")*
- The first argument is the name of the destination SQLite database.
- The second argument is the name of the table that will be cleared inside the SQLite database.

# FR
# Packet pour extraire et stocker les différentes données des réseaux sociaux dans une base de données communes


## Guide pour bien démarrer :
**Étape 1)** Télécharger le projet complet sous la forme d'un zip (le bouton vert en haut à droite).
**Étape 2)** Décompresser le fichier zip dans un dossier vide (le dossier accueillera donc le projet).
**Étape 3)** Ouvrez les fichiers *".py"*.
Vous êtes maintenant prêt à utiliser le packet.

## Comment réaliser un scraping :
### Phase 1 (Extraction en csv)
#### (L'objectif est d'abord d'accumuler les données des réseaux sociaux dans des fichiers csv).
**Étape 1)** Ouvrez le fichier *"superfunction.py"*.
**Étape 2)** Écrivez votre requête en la construisant de cette façon :
*scrapeMediaPostBySearch("vacciné", count=50, post_file="vaccin_table_post.csv", profile_file= "vaccin_table_profile.csv")*
- Le premier argument est le mot clé qui sera recherché, ici, c'est le mot "vacciné".
- Le second argument est le nombre maximum de postes qui seront recherché (par réseaux sociaux).
- Le troisième argument est le nom du fichier CSV qui sera créé pour stocker les postes.
- Le quatrième argument est le nom du fichier CSV qui sera créé pour stocker les profils.

**Étape 3)** Recommencer l'étape 2 avec un mot clé différent pour accumuler les données dans les même fichiers csv.

### Phase 2 (Préparer la base de données SQLite)
#### (Pour pouvoir stocker les données, il est nécessaire d'avoir une base donnée SQLite prête).
**Étape 1)** Copier le modèle vide de base de données SQLite intitulé *"sqlite_template.db"*.
**Étape 2)** Renommez le fichier selon votre convenance, exemple : *"vaccin_sqlite.db"*.

### Phase 3 (Stockage en SQLite)
#### (Maintenant que les fichiers csv sont créé, il faut injecter les fichiers csv dans une base de données SQLite).
**Étape 1)** Ouvrez le fichier *"csv_to_sql.py"*.
**Étape 2)** Écrivez votre requête en la construisant de cette façon :
pour les profiles : *csvToSqlite("vaccin_table_profile","vaccin_db", "table_profile", profile_structure)*
pour les postes : *csvToSqlite("vaccin_table_post","vaccin_db", "table_post", post_structure)*
- Le premier argument est le nom du fichier csv qui va être transféré (le nom sans le *".csv"*).
- Le second argument est le nom de la base de données SQLite destinataire.
- Le troisième argument est le nom de la table destinataire à l'intérieur de la base SQLite (il y en deux : *"table_profile"* pour les profils et *"table_post"* pour les postes).
- Le quatrième argument correspond à la structure des données du fichier csv et de la table (il y en a deux : *"profile_structure"* pour les profils et *"post_structure"* pour les postes).

**Étape 3)** Pour effacer une table dans la base SQLite, utilisez la fonction : *resetTable("vaccin_db","table_profile")*
- Le premier argument est le nom de la base de données SQLite destinataire.
- Le second argument est le nom de la table qui va être effacé à l'intérieur de la base SQLite.
