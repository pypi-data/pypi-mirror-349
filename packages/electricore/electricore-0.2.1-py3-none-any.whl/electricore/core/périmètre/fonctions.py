import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from electricore.core.périmètre.modèles import HistoriquePérimètre, SituationPérimètre, ModificationContractuelleImpactante
from electricore.core.relevés.modèles import RelevéIndex

@pa.check_types
def extraire_situation(date: pd.Timestamp, historique: DataFrame[HistoriquePérimètre]) -> DataFrame[SituationPérimètre]:
    """
    Extrait la situation du périmètre à une date donnée.
    
    Args:
        date (pd.Timestamp): La date de référence.
        historique (pd.DataFrame): L'historique des événements contractuels.

    Returns:
        pd.DataFrame: Une vue du périmètre à `date`, conforme à `SituationPérimètre`.
    """
    return (
        historique[historique["Date_Evenement"] <= date]
        .sort_values(by="Date_Evenement", ascending=False)
        .drop_duplicates(subset=["Ref_Situation_Contractuelle"], keep="first")
    )
@pa.check_types
def extraire_historique_à_date(
    historique: DataFrame[HistoriquePérimètre],
    fin: pd.Timestamp
) -> DataFrame[HistoriquePérimètre]:
    """
    Extrait uniquement les variations (changements contractuels) qui ont eu lieu dans une période donnée.

    Args:
        deb (pd.Timestamp): Début de la période.
        fin (pd.Timestamp): Fin de la période.
        historique (pd.DataFrame): Historique des événements contractuels.

    Returns:
        pd.DataFrame: Un sous-ensemble de l'historique contenant uniquement les variations dans la période.
    """
    return historique[
        (historique["Date_Evenement"] <= fin)
    ].sort_values(by="Date_Evenement", ascending=True)  # Trie par ordre chronologique

@pa.check_types
def extraire_période(
    deb: pd.Timestamp, fin: pd.Timestamp, 
    historique: DataFrame[HistoriquePérimètre]
) -> DataFrame[HistoriquePérimètre]:
    """
    Extrait uniquement les variations (changements contractuels) qui ont eu lieu dans une période donnée.

    Args:
        deb (pd.Timestamp): Début de la période.
        fin (pd.Timestamp): Fin de la période.
        historique (pd.DataFrame): Historique des événements contractuels.

    Returns:
        pd.DataFrame: Un sous-ensemble de l'historique contenant uniquement les variations dans la période.
    """
    return historique[
        (historique["Date_Evenement"] >= deb) & (historique["Date_Evenement"] <= fin)
    ].sort_values(by="Date_Evenement", ascending=True)  # Trie par ordre chronologique

@pa.check_types
def extraite_relevés_entrées(
    historique: DataFrame[HistoriquePérimètre]
) -> DataFrame[RelevéIndex]:
        _événements = ['MES', 'PMES', 'CFNE']
        _colonnes_meta_releve = ['Ref_Situation_Contractuelle', 'pdl', 'Unité', 'Précision', 'Source']
        _colonnes_relevé = ['Id_Calendrier_Distributeur', 'Date_Releve', 'Nature_Index', 'HP', 'HC', 'HCH', 'HPH', 'HPB', 'HCB', 'BASE']
        _colonnes_relevé_après = ['Après_'+c for c in _colonnes_relevé]
        return RelevéIndex.validate(
            historique[historique['Evenement_Declencheur'].isin(_événements)][_colonnes_meta_releve + _colonnes_relevé_après]
            .rename(columns={k: v for k,v in zip(_colonnes_relevé_après, _colonnes_relevé)})
            .dropna(subset=['Date_Releve'])
            )

@pa.check_types
def extraite_relevés_sorties(
    historique: DataFrame[HistoriquePérimètre]
) -> DataFrame[RelevéIndex]:
        _événements = ['RES', 'CFNS']
        _colonnes_meta_releve = ['Ref_Situation_Contractuelle', 'pdl', 'Unité', 'Précision', 'Source']
        _colonnes_relevé = ['Id_Calendrier_Distributeur', 'Date_Releve', 'Nature_Index', 'HP', 'HC', 'HCH', 'HPH', 'HPB', 'HCB', 'BASE']
        _colonnes_relevé_avant = ['Avant_'+c for c in _colonnes_relevé]
        return RelevéIndex.validate(
            historique[historique['Evenement_Declencheur'].isin(_événements)][_colonnes_meta_releve + _colonnes_relevé_avant]
            .rename(columns={k: v for k,v in zip(_colonnes_relevé_avant, _colonnes_relevé)})
            .dropna(subset=['Date_Releve'])
            )

@pa.check_types
def extraire_modifications_impactantes(
    deb: pd.Timestamp,
    historique: DataFrame[HistoriquePérimètre]
) -> DataFrame[ModificationContractuelleImpactante]:
    """
    Détecte les MCT dans une période donnée et renvoie les variations de Puissance_Souscrite
    et Formule_Tarifaire_Acheminement avant et après chaque MCT.

    Args:
        deb (pd.Timestamp): Début de la période.
        historique (pd.DataFrame): Historique des événements contractuels.

    Returns:
        DataFrame[ModificationContractuelleImpactante]: DataFrame contenant les MCT avec les valeurs avant/après.
    """

    # 🔍 Décaler les valeurs pour obtenir les données "avant" AVANT de filtrer
    historique = historique.sort_values(by=["Ref_Situation_Contractuelle", "Date_Evenement"])
    historique["Avant_Puissance_Souscrite"] = historique.groupby("Ref_Situation_Contractuelle")["Puissance_Souscrite"].shift(1)
    historique["Avant_Formule_Tarifaire_Acheminement"] = historique.groupby("Ref_Situation_Contractuelle")["Formule_Tarifaire_Acheminement"].shift(1)


    # 📌 Filtrer uniquement les MCT dans la période donnée
    impacts = (
          historique[
            (historique["Date_Evenement"] >= deb) &
            (historique["Evenement_Declencheur"] == "MCT")]
          .copy()
          .rename(columns={'Puissance_Souscrite': 'Après_Puissance_Souscrite', 'Formule_Tarifaire_Acheminement':'Après_Formule_Tarifaire_Acheminement'})
          .drop(columns=['Segment_Clientele', 'Num_Depannage', 'Categorie', 'Etat_Contractuel', 'Type_Compteur', 'Date_Derniere_Modification_FTA', 'Type_Evenement', 'Ref_Demandeur', 'Id_Affaire'])
    )
    
    # TODO: Prendre en compte plus de cas
    impacts['Impacte_energies'] = (
        impacts["Avant_Id_Calendrier_Distributeur"].notna() & 
        impacts["Après_Id_Calendrier_Distributeur"].notna() & 
        (impacts["Avant_Id_Calendrier_Distributeur"] != impacts["Après_Id_Calendrier_Distributeur"])
    )

    # ➕ Ajout de la colonne de lisibilité du changement
    def generer_resumé(row):
        modifications = []
        if row["Avant_Puissance_Souscrite"] != row["Après_Puissance_Souscrite"]:
            modifications.append(f"P: {row['Avant_Puissance_Souscrite']} → {row['Après_Puissance_Souscrite']}")
        if row["Avant_Formule_Tarifaire_Acheminement"] != row["Après_Formule_Tarifaire_Acheminement"]:
            modifications.append(f"FTA: {row['Avant_Formule_Tarifaire_Acheminement']} → {row['Après_Formule_Tarifaire_Acheminement']}")
        return ", ".join(modifications) if modifications else "Aucun changement"
    
    impacts["Résumé_Modification"] = impacts.apply(generer_resumé, axis=1)

    ordre_colonnes = ModificationContractuelleImpactante.to_schema().columns.keys()
    impacts = impacts[ordre_colonnes]
    
    return impacts

@pa.check_types
def detecter_points_de_rupture(historique: DataFrame[HistoriquePérimètre]) -> DataFrame[HistoriquePérimètre]:
    """
    Enrichit l'historique avec les colonnes d'impact (turpe, énergie, turpe_variable) et un résumé des modifications.
    Toutes les lignes sont conservées.

    Args:
        historique (pd.DataFrame): Historique complet des événements contractuels.

    Returns:
        pd.DataFrame: Historique enrichi avec détection des ruptures et résumé humain.
    """
    index_cols = ['BASE', 'HP', 'HC', 'HPH', 'HCH', 'HPB', 'HCB']

    historique = historique.sort_values(by=["Ref_Situation_Contractuelle", "Date_Evenement"]).copy()
    historique["Avant_Puissance_Souscrite"] = historique.groupby("Ref_Situation_Contractuelle")["Puissance_Souscrite"].shift(1)
    historique["Avant_Formule_Tarifaire_Acheminement"] = historique.groupby("Ref_Situation_Contractuelle")["Formule_Tarifaire_Acheminement"].shift(1)

    impact_turpe_fixe = (
        (historique["Avant_Puissance_Souscrite"].notna() &
         (historique["Avant_Puissance_Souscrite"] != historique["Puissance_Souscrite"])) |
        (historique["Avant_Formule_Tarifaire_Acheminement"].notna() &
         (historique["Avant_Formule_Tarifaire_Acheminement"] != historique["Formule_Tarifaire_Acheminement"]))
    )

    impact_energie = (
        (historique["Avant_Id_Calendrier_Distributeur"].notna() &
         historique["Après_Id_Calendrier_Distributeur"].notna() &
         (historique["Avant_Id_Calendrier_Distributeur"] != historique["Après_Id_Calendrier_Distributeur"])) |
        pd.concat([
            (historique[f"Avant_{col}"].notna() &
             historique[f"Après_{col}"].notna() &
             (historique[f"Avant_{col}"] != historique[f"Après_{col}"]))
            for col in index_cols
        ], axis=1).any(axis=1)
    )

    impact_turpe_variable = (
      (impact_energie) |
      (historique["Avant_Formule_Tarifaire_Acheminement"].notna() &
         (historique["Avant_Formule_Tarifaire_Acheminement"] != historique["Formule_Tarifaire_Acheminement"]))
    )

    historique["impact_turpe_fixe"] = impact_turpe_fixe
    historique["impact_energie"] = impact_energie
    historique["impact_turpe_variable"] = impact_turpe_variable

    def generer_resume(row):
        modifs = []
        if row["impact_turpe_fixe"]:
            if pd.notna(row.get("Avant_Puissance_Souscrite")) and row["Avant_Puissance_Souscrite"] != row["Puissance_Souscrite"]:
                modifs.append(f"P: {row['Avant_Puissance_Souscrite']} → {row['Puissance_Souscrite']}")
            if pd.notna(row.get("Avant_Formule_Tarifaire_Acheminement")) and row["Avant_Formule_Tarifaire_Acheminement"] != row["Formule_Tarifaire_Acheminement"]:
                modifs.append(f"FTA: {row['Avant_Formule_Tarifaire_Acheminement']} → {row['Formule_Tarifaire_Acheminement']}")
        if row["impact_energie"]:
            modifs.append("rupture index")
        return ", ".join(modifs) if modifs else ""

    historique["resume_modification"] = historique.apply(generer_resume, axis=1)

    return historique.reset_index(drop=True)