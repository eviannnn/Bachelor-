import os
from dotenv import load_dotenv
from openai import OpenAI
from anonymizer import ProjectAnonymizer

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")


class RequirementsAgent:
    def __init__(self):
        self.anonymizer = ProjectAnonymizer()
        self.original_project_text = self.load_project()
        self.project_text = self.anonymizer.anonymize(self.original_project_text)
        self.save("anonymized_project_description.txt", self.project_text)

    def load_project(self):
        with open("input/project_description.txt", "r", encoding="utf-8") as f:
            return f.read()

    def ask_llm(self, system_prompt, user_prompt):
        response = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return response.output[0].content[0].text

    def functional_agent(self):
        system = "Tu esi pieredzējis programmatūras sistēmu analītiķis."
        user = f"""
Pamatojoties uz projekta aprakstu, ģenerē funkcionālās prasības.

Prasību noformējums:
- Katru prasību raksti atsevišķā punktā
- Sāc ar “Sistēmai jāspēj…”

Projekta apraksts:
{self.project_text}
"""
        return self.ask_llm(system, user)

    def nonfunctional_agent(self):
        system = "Tu esi programmatūras arhitekts un kvalitātes inženieris."
        user = f"""
Pamatojoties uz projekta aprakstu, ģenerē nefunkcionālās prasības.

Iekļauj:
- veiktspēja
- drošība
- lietojamība
- uzticamība
- mērogojamība

Prasībām jābūt izmērāmām.

Projekta apraksts:
{self.project_text}
"""
        return self.ask_llm(system, user)

    def user_stories_agent(self):
        system = "Tu esi produktu īpašnieks (Product Owner)."
        user = f"""
Izveido lietotāju stāstus.

Formāts:
“Kā [lietotājs], es vēlos…, lai…”

Katram lietotāju stāstam:
- pievieno 2–3 acceptance criteria

Projekta apraksts:
{self.project_text}
"""
        return self.ask_llm(system, user)

    def use_cases_agent(self):
        system = "Tu esi biznesa analītiķis."
        user = f"""
Izveido use case scenārijus.

Katram lietošanas gadījumam norādi:
- nosaukumu
- aktoru
- īsu aprakstu
- galvenos soļus

Projekta apraksts:
{self.project_text}
"""
        return self.ask_llm(system, user)

    def mermaid_diagram_agent(self, functional, usecases):
        system = "Tu esi sistēmu analītiķis, kas veido Mermaid diagrammas prasību vizualizācijai."
        user = f"""
Balstoties uz funkcionālajām prasībām un lietošanas gadījumiem, izveido Mermaid diagrammu.

Uzdevums:
- identificē galvenos aktorus;
- identificē galvenās sistēmas funkcijas;
- izveido Mermaid flowchart diagrammu;
- diagrammai jābūt pārskatāmai;
- neizdomā funkcijas, kuru nav ievaddatos;
- neatkārto vienādas funkcijas;
- atgriez tikai Mermaid kodu bez papildu paskaidrojumiem;
- nesāc ar ```mermaid un nebeidz ar ```.

Funkcionālās prasības:
{functional}

Lietošanas gadījumi:
{usecases}
"""
        return self.ask_llm(system, user)

    def validation_agent(self, artifact_name, artifact_text):
        system = "Tu esi pieredzējis prasību analītiķis un kvalitātes eksperts."
        user = f"""
Tavs uzdevums ir validēt šo artefaktu: {artifact_name}

Validē saturu pēc ISO/IEC/IEEE 29148:2018 kvalitātes kritērijiem.

Kritēriji:
- Nepieciešamība (necessary)
- Nepārprotamība (unambiguous)
- Pilnīgums (complete)
- Realizējamība (feasible)
- Pārbaudāmība (verifiable)
- Korektums (correct)
- Viennozīmīgums (singular)

Ievaddati:
{artifact_text}

Katram punktam:
1. Novērtē kritērijus
2. Identificē problēmas
3. Piedāvā uzlabotu versiju

Beigās sniedz īsu kopsavilkumu:
- kopējā kvalitāte
- galvenās problēmas
- vai artefakts ir izmantojams tālākai projektēšanai
"""
        return self.ask_llm(system, user)

    def create_final_document(
        self,
        functional,
        nonfunctional,
        stories,
        usecases,
        mermaid_diagram,
        validation_functional,
        validation_nonfunctional,
        validation_user_stories,
        validation_use_cases
    ):
        return f"""
# Prasību analīzes gala dokuments

## 1. Projekta apraksts

{self.project_text}

---

## 2. Funkcionālās prasības

{functional}

---

## 3. Nefunkcionālās prasības

{nonfunctional}

---

## 4. Lietotāju stāsti

{stories}

---

## 5. Lietošanas gadījumi

{usecases}

---

## 6. Mermaid lietošanas gadījumu diagramma

~~~mermaid
{mermaid_diagram}
~~~

---

# 7. Validācijas rezultāti

## 7.1. Funkcionālo prasību validācija

{validation_functional}

---

## 7.2. Nefunkcionālo prasību validācija

{validation_nonfunctional}

---

## 7.3. Lietotāju stāstu validācija

{validation_user_stories}

---

## 7.4. Lietošanas gadījumu validācija

{validation_use_cases}

---

## 8. Kopējais secinājums

Izstrādātais vairāku aģentu risinājums ģenerēja vairākus prasību dokumentācijas artefaktus: funkcionālās prasības, nefunkcionālās prasības, lietotāju stāstus, lietošanas gadījumus un Mermaid lietošanas gadījumu diagrammu. Teksta artefaktus ģenerēja specializēti aģenti, savukārt Mermaid diagrammas ģenerēšanas modulis tika izmantots prasību vizuālai strukturēšanai.

Katrs teksta artefakts tika pārbaudīts ar validācijas aģentu, izmantojot ISO/IEC/IEEE 29148:2018 kvalitātes kritērijus. Validācijas rezultāti parāda, ka ģenerētie artefakti ir izmantojami kā sākotnējā prasību dokumentācijas versija, tomēr pirms tālākas projektēšanas nepieciešama cilvēka pārbaude un atsevišķu prasību precizēšana.

Mermaid diagramma netiek uzskatīta par galīgu projektēšanas modeli, bet gan par sākotnēju vizualizācijas artefaktu, kas palīdz pārskatāmāk attēlot sistēmas funkcijas un aktoru mijiedarbību ar sistēmu.
"""

    def run(self):
        print("Running generation agents...")

        functional = self.functional_agent()
        nonfunctional = self.nonfunctional_agent()
        stories = self.user_stories_agent()
        usecases = self.use_cases_agent()
        mermaid_diagram = self.mermaid_diagram_agent(functional, usecases)

        self.save("functional.txt", functional)
        self.save("nonfunctional.txt", nonfunctional)
        self.save("user_stories.txt", stories)
        self.save("use_cases.txt", usecases)
        self.save("mermaid_use_case_diagram.md", f"```mermaid\n{mermaid_diagram}\n```")

        print("Running validation agents...")

        validation_functional = self.validation_agent("FUNCTIONAL REQUIREMENTS", functional)
        validation_nonfunctional = self.validation_agent("NON-FUNCTIONAL REQUIREMENTS", nonfunctional)
        validation_user_stories = self.validation_agent("USER STORIES", stories)
        validation_use_cases = self.validation_agent("USE CASES", usecases)

        self.save("validation_functional.txt", validation_functional)
        self.save("validation_nonfunctional.txt", validation_nonfunctional)
        self.save("validation_user_stories.txt", validation_user_stories)
        self.save("validation_use_cases.txt", validation_use_cases)

        final_document = self.create_final_document(
            functional,
            nonfunctional,
            stories,
            usecases,
            mermaid_diagram,
            validation_functional,
            validation_nonfunctional,
            validation_user_stories,
            validation_use_cases
        )

        self.save("final_requirements_document.md", final_document)

        print("Done. Final document saved as output/final_requirements_document.md")

    def save(self, filename, content):
        os.makedirs("output", exist_ok=True)
        with open(f"output/{filename}", "w", encoding="utf-8") as f:
            f.write(content)


if __name__ == "__main__":
    agent = RequirementsAgent()
    agent.run()
