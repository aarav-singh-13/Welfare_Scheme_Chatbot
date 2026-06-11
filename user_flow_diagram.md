# Welfare Scheme Chatbot User Flow

This diagram illustrates how the conversational AI adapts its eligibility flow based on three distinct user personas. The backend uses RAG (Retrieval-Augmented Generation) to ground the AI's responses strictly to our scheme database.

```mermaid
graph TD
    A[User sends WhatsApp Message<br/>e.g. 'Hi, schemes ke baare mein batao'] --> B{Language & Intent Detection}
    
    B -->|Detects Hindi/Hinglish| C(AI switches to Hindi/Hinglish<br/>and asks for Age & Occupation)
    B -->|Detects English| D(AI switches to English<br/>and asks for Age & Occupation)
    
    C --> E{User Persona Branching}
    D --> E
    
    %% Persona 1: Farmer
    E -->|Persona 1: Farmer| F1[User: 'Main kisan hu, 45 saal ka']
    F1 --> G1[AI asks: 'Kya aapke paas apni zameen hai?']
    G1 --> H1[User: 'Haan']
    H1 --> I1[AI Returns: PM-KISAN & Ayushman Bharat<br/>+ Document Checklist (Aadhaar, Land Papers)]
    
    %% Persona 2: Gig Worker
    E -->|Persona 2: Gig Worker| F2[User: 'I am a 25yo delivery driver']
    F2 --> G2[AI asks: 'Do you have a bank account?']
    G2 --> H2[User: 'Yes']
    H2 --> I2[AI Returns: Atal Pension Yojana & PMSBY<br/>+ Document Checklist (Aadhaar, Bank Acc)]
    
    %% Persona 3: Rural Woman Head of Household
    E -->|Persona 3: Woman HOH| F3[User: 'Main 35 saal ki hu, ghar mein gas connection nahi hai']
    F3 --> G3[AI asks: 'Kya aap BPL card holder hain?']
    G3 --> H3[User: 'Haan']
    H3 --> I3[AI Returns: PM Ujjwala Yojana & PMAY-G<br/>+ Document Checklist (Aadhaar, BPL Card)]
    
    %% Final Action
    I1 --> J[AI: 'Would you like the link to apply for any of these?']
    I2 --> J
    I3 --> J
```

## Flow Mechanics (Under the Hood)
1. **Turn 1 (Greeting):** The LLM detects language (Hindi, English, or Code-mixed) and establishes the persona's core attributes (Age, Occupation).
2. **Turn 2-3 (Clarification):** The LLM dynamically selects follow-up questions (e.g., land ownership for a farmer, BPL status for a homemaker) based *only* on the eligibility criteria defined in `schemes_db.json`.
3. **Turn 4 (Resolution):** The LLM summarizes the eligible schemes and extracts the required documents from the RAG context, presenting them as a neat WhatsApp-friendly list.
