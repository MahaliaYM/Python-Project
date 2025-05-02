# Historical Shark Attack Data Analysis

**Project Goal:** To analyze historical shark attack data to identify patterns that contribute to incident prevention and the implementation of effective safety measures, as well as to raise public awareness.

**Dataset:** Contains 6095 records with detailed information on shark attacks, including date, location, victim activity, species involved, and fatality.

**Preliminary Column Analysis:**

* **Case Number & Date:** `Case Number` appears to be an identifier with duplicates and an inconsistent format compared to `Date`.
* **Year:** Contains `0` values for very old dates. The possibility of grouping them as "Before Year X" or omitting the column if `Date` is sufficient was considered.
* **Type:** Pending analysis of its usefulness.
* **Country, Area, Location:** Plans to complete missing values based on the relationship between these columns.
* **Activity:** Proposed adding the mode for missing values.
* **Name:** Considered not relevant and planned for removal.
* **Sex:** Maintained, and imputation of missing values with the mode or an "Unknown" category was considered.
* **Age:** Maintained, and imputation of missing values with the mean or information from the `Name` column was proposed.
* **Injury:** Maintained, considering extracting information about the severity of the attack from keywords. Its predictability was questioned.
* **Fatal:** Maintained, but filling in missing values is uncertain (linking to `Injury`?).
* **Time:** Initially considered not relevant, but could be reconsidered for hourly analysis.
* **Species:** Crucial for analyzing the most involved species.
* **Investigator or Source, pdf, href (various columns):** Planned for removal due to perceived irrelevance.
* **Original Order:** Maintained.

**Clarified Questions:**

* **Time:** Initially will not be considered, but could be reconsidered.
* **Official Data for Dates:** Agreed to discard years after 1600.
* **Activity and Sex (Imputation):** A comparison will be made between filling with the mode/AI (`Name` for `Sex`) and using "Unknown."
* **Species (Breakdown by Meters):** Exploring the possibility of inferring species based on reported length.

**Initial Task Distribution (April 28th):**

* **Mahalia:** Country, Area, Location, Age.
* **Alexia:** Type, Name, Sex, Injury, Fatal.
* **Alexander:** Date, Year, Activity, Species.

**Redistribution of Tasks (After Starting Data Cleaning):**

* **Mahalia:** Country, Area, Location, Age, **Date, Injury**.
* **Alexia:** Date, Year, Name, Sex, Activity, **Preliminary CSV Cleaning**.
* **Alexander:** Type, Injury, Fatal, Species.

**Detailed Progress by Day:**

* **April 28th:** General analysis of the dataset, initial decisions on column treatment, and Kanban preparation. Redistribution of tasks after identifying dependencies between columns.
* **April 29th:** Continuation of data cleaning, identifying challenges such as inconsistent information in cells and a large number of missing values.
    * **Mahalia:** Completed the treatment of `Age` (imputing means for ranges like "Teen," "20s," etc., and using descriptive information from `Name`). Completed the treatment of `Country`, `Area`, and `Location` by imputing the mode by groupings. Progress was made on treating `Date` (standardizing formats, extracting years, keeping ranges like "1920s" as they are).
    * **Alexia:** Completed the treatment of `Activity` using keyBERT to extract keywords and AI to reclassify activities. Completed the treatment of `Sex` using keyBERT and gender-guesser from `Name`, creating two columns for missing value imputation (mode vs. "Unknown").
    * **Alexander:** Identified significant roadblocks in `Injury` and `Species` due to a lack of coherent information and missing values. Also noted problems with inconsistent formats in `Date`.
* **April 30th:** Restructuring of task distribution to address roadblocks.
    * **Mahalia:** Finalized the treatment of `Date` (standardization, year extraction, discarding problematic records). Treated `Injury` by imputing "Fatal" if `Fatal` was "Y" and "Unknown" for the rest of the missing values.
    * **Alexia:** Provided code for preliminary CSV cleaning, removing unnecessary columns and renaming others.
    * **Alexander:** Continued working on the treatment of `Species`.

**Roadblocks Encountered and Resolved:**

* **Initial Roadblocks:** Missing values in `Injury`, difficulties with the classification and treatment of `Species`, inconsistent formats in `Date`.
* **Partial/Total Solutions:**
    * `Injury`: Missing values will be completed with "Unknown" or "Fatal" based on the `Fatal` column.
    * `Date`: A more in-depth breakdown was carried out to process the data, successfully standardizing formats and extracting useful information.
    * `Species`: In progress.

**Next Steps:**

* **Begin exploratory data analysis (EDA):** Once cleaning is sufficient, start looking for patterns in the key variables (date, location, activity, species, fatality).
* **Answer the initial project questions:**
    * Temporal trends in the frequency of attacks.
    * Locations with the highest incidence and possible factors.
    * Relationships between victims and involved species.
* **Develop mitigation strategies and awareness recommendations.**
