import type { Locale } from "./site";

export type ServiceOffering = {
  id: string;
  title: string;
  summary: string;
  body: string;
};

export type FaqItem = {
  id: string;
  question: string;
  answer: string;
};

export type PageSeo = {
  title: string;
  description: string;
};

export type OfferingsCopy = {
  servicesTagline: string;
  servicesKicker: string;
  servicesTitle: string;
  servicesIntro: string;
  servicesCta: string;
  servicesPageTitle: string;
  servicesPageLede: string;
  servicesProofLabel: string;
  servicesBackHome: string;
  servicesContactCta: string;
  faqKicker: string;
  faqTitle: string;
  faqLede: string;
  faqContactCta: string;
  faqBackHome: string;
  contactFaqLabel: string;
  offerings: ServiceOffering[];
  faqs: FaqItem[];
  pageSeo: {
    home: PageSeo;
    services: PageSeo;
    faq: PageSeo;
  };
};

export const offeringsByLocale: Record<Locale, OfferingsCopy> = {
  el: {
    servicesTagline: "Παροχή Υπηρεσιών Πληροφορικής & Λογισμικού",
    servicesKicker: "03 — Υπηρεσίες",
    servicesTitle: "Υπηρεσίες που προσφέρουμε",
    servicesIntro:
      "Υπηρεσίες πληροφορικής και λογισμικού: ανάπτυξη ιστοσελίδων, e-shops, εφαρμογές κατά παραγγελία, συμβουλές συστημάτων, QR & NFC κάρτες και SEO & AEO.",
    servicesCta: "Δες όλες τις υπηρεσίες",
    servicesPageTitle: "Υπηρεσίες πληροφορικής & λογισμικού",
    servicesPageLede:
      "Ανάπτυξη website, προγραμματισμός και συμβουλευτική για επιχειρήσεις στην Ελλάδα — από την πρώτη ιδέα μέχρι τη δημοσίευση και τη βελτιστοποίηση.",
    servicesProofLabel: "Δες επιλεγμένα έργα",
    servicesBackHome: "Πίσω στο portfolio",
    servicesContactCta: "Ζήτα προσφορά",
    faqKicker: "Συχνές ερωτήσεις",
    faqTitle: "Συχνές ερωτήσεις",
    faqLede:
      "Σύντομες απαντήσεις για ανάπτυξη ιστοσελίδων, χρονοδιαγράμματα, συνεργασία από την Αθήνα και απομακρυσμένα, και πώς ξεκινά ένα έργο.",
    faqContactCta: "Επικοινώνησε",
    faqBackHome: "Πίσω στο portfolio",
    contactFaqLabel: "Συχνές ερωτήσεις",
    offerings: [
      {
        id: "websites",
        title: "Ιστοσελίδες & E-shops",
        summary: "Σύγχρονες, γρήγορες ιστοσελίδες και ηλεκτρονικά καταστήματα.",
        body: "Σχεδιασμός και ανάπτυξη ιστοσελίδων και e-shops με έμφαση στην ταχύτητα, την εμφάνιση σε κινητά και την καθαρή δομή περιεχομένου. Ιδανικό για επαγγελματίες και μικρές επιχειρήσεις που θέλουν παρουσία στο web και ανάπτυξη website από το μηδέν ή ανανέωση υπάρχουσας σελίδας.",
      },
      {
        id: "custom-apps",
        title: "Εφαρμογές κατά παραγγελία",
        summary:
          "Web εφαρμογές με Vue/Nuxt ή React/Next, προσαρμοσμένες στη ροή σας.",
        body: "Προγραμματισμός και ανάπτυξη web εφαρμογών κατά παραγγελία — πίνακες διαχείρισης, πλατφόρμες, εργαλεία για ομάδες. Δουλεύω με Vue, Nuxt, React και Next.js, με καθαρό κώδικα και προτεραιότητα στη χρηστικότητα.",
      },
      {
        id: "consulting",
        title: "Συμβουλές συστημάτων & λογισμικού",
        summary:
          "Επιλογή stack, αρχιτεκτονική και ανάλυση δεδομένων όπου χρειάζεται.",
        body: "Συμβουλευτική για συστήματα και λογισμικό: τι να χτίσετε, με ποια εργαλεία, και πώς να οργανώσετε δεδομένα και αναφορές. Συνδυασμός εμπειρίας σε web development και ανάλυσης δεδομένων (Python, SQL, BI) για πρακτικές αποφάσεις και ξεκάθαρους στόχους.",
      },
      {
        id: "smart-cards",
        title: "Έξυπνες κάρτες QR & NFC",
        summary: "Ψηφιακές κάρτες και σελίδες προορισμού για QR ή και NFC.",
        body: "Σχεδιασμός και υλοποίηση έξυπνων καρτών με QR ή και NFC που οδηγούν σε σελίδες της επιλογής σας ή απευθείας σε κριτικές Google.",
      },
      {
        id: "seo-aeo",
        title: "SEO & AEO",
        summary:
          "Βελτιστοποίηση για μηχανές αναζήτησης και απαντητικές / AI εμπειρίες.",
        body: "Τεχνικό SEO και AEO (answer engine optimization): metadata, δομή σελίδων, schema, ταχύτητα και περιεχόμενο που απαντά σε πραγματικές ερωτήσεις πελατών — για εμφάνιση σε Google και σε AI απαντήσεις, στα ελληνικά και στα αγγλικά.",
      },
    ],
    faqs: [
      {
        id: "what-you-build",
        question: "Τι υπηρεσίες πληροφορικής προσφέρετε;",
        answer:
          "Ανάπτυξη ιστοσελίδων και e-shops, εφαρμογές κατά παραγγελία (Vue/Nuxt, React/Next), συμβουλές συστημάτων και λογισμικού, έξυπνες κάρτες QR & NFC, και SEO & AEO. Η έδρα είναι στην Αθήνα· συνεργάζομαι και απομακρυσμένα σε όλη την Ελλάδα.",
      },
      {
        id: "timeline",
        question: "Πόσο διαρκεί η ανάπτυξη ενός website;",
        answer:
          "Ένα απλό επαγγελματικό website συχνά ολοκληρώνεται σε λίγες εβδομάδες. E-shops και custom εφαρμογές χρειάζονται περισσότερο χρόνο ανάλογα με λειτουργίες και περιεχόμενο. Στα πρώτα στάδια επικοινωνίας συμφωνούμε στους στόχους και σε ένα ενδεικτικό χρονοδιάγραμμα.",
      },
      {
        id: "process",
        question: "Πώς ξεκινάει ένα έργο;",
        answer:
          "Ξεκινάμε με σύντομη συζήτηση για στόχους, κοινό και παραδείγματα που σας αρέσουν. Ακολουθεί πρόταση με εύρος και εκτίμηση παράδοσης. Μετά ξεκινάει ο σχεδιασμός και η ανάπτυξη με ενδιάμεσα checkpoints, και τέλος δημοσίευση, βασικό SEO και παράδοση.",
      },
      {
        id: "remote",
        question: "Δουλεύετε μόνο στην Αθήνα;",
        answer:
          "Βρίσκομαι στην Αθήνα και συναντήσεις μπορούν να γίνουν δια ζώσης όταν χρειάζεται. Τα περισσότερα έργα τρέχουν απομακρυσμένα με τηλέφωνο, email και βιντεοκλήσεις, για πελάτες σε όλη την Ελλάδα.",
      },
      {
        id: "stack",
        question: "Με ποιες τεχνολογίες δουλεύετε;",
        answer:
          "Κυρίως σύγχρονο web: Vue, Nuxt, React, Next.js, TypeScript και Tailwind. Για δεδομένα και αναφορές χρησιμοποιώ Python, SQL και εργαλεία BI όταν το έργο το απαιτεί.",
      },
      {
        id: "seo-included",
        question: "Περιλαμβάνεται SEO στην ανάπτυξη ιστοσελίδας;",
        answer:
          "Κάθε νέο site στήνεται με σωστά titles, περιγραφές, δομή headings, canonical και βασικό τεχνικό SEO. Πιο βαθύ SEO & AEO (λέξεις-κλειδιά, schema, περιεχόμενο για AI απαντήσεις) μπορεί να προστεθεί ως ξεχωριστή ή επιπλέον υπηρεσία.",
      },
    ],
    pageSeo: {
      home: {
        title:
          "Αντώνης Σκαρλάτος | Υπηρεσίες πληροφορικής & ανάπτυξη website Αθήνα",
        description:
          "Παροχή υπηρεσιών πληροφορικής και λογισμικού στην Αθήνα: ανάπτυξη ιστοσελίδων, e-shops, εφαρμογές, συμβουλές, QR/NFC και SEO & AEO. Antonis Skarlatos — web developer.",
      },
      services: {
        title:
          "Υπηρεσίες πληροφορικής | Ανάπτυξη website & εφαρμογές — Αντώνης Σκαρλάτος",
        description:
          "Ιστοσελίδες & e-shops, εφαρμογές κατά παραγγελία, συμβουλές συστημάτων, έξυπνες κάρτες QR & NFC, SEO & AEO. Website development και προγραμματισμός στην Αθήνα.",
      },
      faq: {
        title:
          "Συχνές ερωτήσεις | Υπηρεσίες web & πληροφορικής — Αντώνης Σκαρλάτος",
        description:
          "Απαντήσεις για ανάπτυξη ιστοσελίδων, χρονοδιαγράμματα, τεχνολογίες, απομακρυσμένη συνεργασία και SEO στην Αθήνα και την Ελλάδα.",
      },
    },
  },
  en: {
    servicesTagline: "IT & software services",
    servicesKicker: "03 — Services",
    servicesTitle: "Services we offer",
    servicesIntro:
      "IT and software services: website development, e-shops, custom apps, systems consulting, QR & NFC cards, and SEO & AEO.",
    servicesCta: "See all services",
    servicesPageTitle: "IT & software services",
    servicesPageLede:
      "Website development, programming, and consulting for businesses in Greece — from the first idea through launch and optimisation.",
    servicesProofLabel: "See selected work",
    servicesBackHome: "Back to portfolio",
    servicesContactCta: "Request a quote",
    faqKicker: "Frequently asked questions",
    faqTitle: "Frequently asked questions",
    faqLede:
      "Short answers on website development, timelines, working from Athens or remotely, and how a project starts.",
    faqContactCta: "Get in touch",
    faqBackHome: "Back to portfolio",
    contactFaqLabel: "Frequently asked questions",
    offerings: [
      {
        id: "websites",
        title: "Websites & e-shops",
        summary: "Modern, fast websites and online stores.",
        body: "Design and development of websites and e-shops with a focus on speed, mobile presentation, and clear content structure. Ideal for professionals and small businesses that want a web presence — a new website from scratch or a refresh of an existing one.",
      },
      {
        id: "custom-apps",
        title: "Custom applications",
        summary:
          "Web apps with Vue/Nuxt or React/Next, tailored to your workflow.",
        body: "Programming and development of custom web applications — dashboards, platforms, team tools. I work with Vue, Nuxt, React, and Next.js, with clean code and usability first.",
      },
      {
        id: "consulting",
        title: "Systems & software consulting",
        summary: "Stack choices, architecture, and data analytics when needed.",
        body: "Consulting on systems and software: what to build, which tools to use, and how to organise data and reporting. A combination of web development and data analytics experience (Python, SQL, BI) for practical decisions and clear goals.",
      },
      {
        id: "smart-cards",
        title: "Smart QR & NFC cards",
        summary: "Digital cards and landing pages for QR and/or NFC.",
        body: "Design and implementation of smart cards with QR and/or NFC that lead to pages of your choice, or directly to Google reviews.",
      },
      {
        id: "seo-aeo",
        title: "SEO & AEO",
        summary: "Optimisation for search engines and answer / AI experiences.",
        body: "Technical SEO and AEO (answer engine optimisation): metadata, page structure, schema, performance, and content that answers real customer questions — for visibility in Google and AI answers, in Greek and English.",
      },
    ],
    faqs: [
      {
        id: "what-you-build",
        question: "What IT services do you offer?",
        answer:
          "Website and e-shop development, custom applications (Vue/Nuxt, React/Next), systems and software consulting, smart QR & NFC cards, and SEO & AEO. Based in Athens; I also work remotely across Greece.",
      },
      {
        id: "timeline",
        question: "How long does website development take?",
        answer:
          "A simple professional website often finishes in a few weeks. E-shops and custom apps take longer depending on features and content. In the early stages of communication we agree on goals and an indicative timeline.",
      },
      {
        id: "process",
        question: "How does a project start?",
        answer:
          "We start with a short discussion about goals, audience, and examples you like. A proposal follows with scope and a delivery estimate. Then design and development begin with intermediate checkpoints, and finally launch, baseline SEO, and handover.",
      },
      {
        id: "remote",
        question: "Do you only work in Athens?",
        answer:
          "I am based in Athens and meetings can happen in person when needed. Most projects run remotely by phone, email, and video calls, for clients across Greece.",
      },
      {
        id: "stack",
        question: "Which technologies do you use?",
        answer:
          "Mainly modern web: Vue, Nuxt, React, Next.js, TypeScript, and Tailwind. For data and reporting I use Python, SQL, and BI tools when the project needs them.",
      },
      {
        id: "seo-included",
        question: "Is SEO included with a new website?",
        answer:
          "Every new site is set up with proper titles, descriptions, heading structure, canonicals, and baseline technical SEO. Deeper SEO & AEO (keywords, schema, content for AI answers) can be added as a separate or extra service.",
      },
    ],
    pageSeo: {
      home: {
        title:
          "Antonis Skarlatos | IT services & website development in Athens",
        description:
          "IT and software services in Athens: website development, e-shops, apps, consulting, QR/NFC, and SEO & AEO. Antonis Skarlatos — web developer.",
      },
      services: {
        title: "IT services | Website development & apps — Antonis Skarlatos",
        description:
          "Websites & e-shops, custom applications, systems consulting, smart QR & NFC cards, SEO & AEO. Website development and programming in Athens.",
      },
      faq: {
        title:
          "Frequently asked questions | Web & IT services — Antonis Skarlatos",
        description:
          "Answers on website development, timelines, technologies, remote collaboration, and SEO in Athens and across Greece.",
      },
    },
  },
};
