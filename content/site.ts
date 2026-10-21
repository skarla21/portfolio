export type Locale = 'el' | 'en'

export type Job = {
  dates: string
  role: string
  place: string
  points: string[]
}

export type Study = {
  dates: string
  credential: string
  school: string
  detail: string
  thesisLabel: string
  thesis: string
  thesisHref?: string
  supervisors: string
}

export type Certificate = {
  label: string
  href?: string
}

export type Project = {
  id: string
  name: string
  dates: string
  stack: string
  summary: string
  href?: string
  accent: string
}

export type Hobby = {
  id: string
  label: string
  image: string
}

export type Copy = {
  name: string
  nameLines: [string, string]
  eyebrow: string
  place: string
  lede: string
  disciplines: string
  viewProjects: string
  scroll: string
  skip: string
  introLabel: string
  profile: string[]
  journeyTitle: string
  journeyLede: string
  supervisorsLabel: string
  languagesLabel: string
  certificatesLabel: string
  education: Study[]
  work: Job[]
  languages: string[]
  certificates: Certificate[]
  skillsLabel: string
  workKicker: string
  workTitle: string
  workIntro: string
  projects: Project[]
  beyondTitle: string
  hobbies: Hobby[]
  contactKicker: string
  contactTitle: string
  cvLabel: string
  cv: string
  address: string
  seoDescription: string
  nav: { href: string; label: string }[]
  email: string
  phone: string
  phoneHref: string
  linkedin: string
  github: string
}

const contact = {
  email: 'antwnis_skarlatos@yahoo.com',
  phone: '+30 6983696885',
  phoneHref: 'tel:+306983696885',
  linkedin: 'https://www.linkedin.com/in/antonis-skarlatos-a41781212',
  github: 'https://github.com/skarla21',
}

const pergamos = 'https://pergamos.lib.uoa.gr/en/item/uoadl:3310771#fields'

const certificates = {
  typescript: 'https://www.udemy.com/certificate/UC-d8081898-9d6a-46e3-9cad-bfdedab01cae/',
  bootcamp: 'https://www.udemy.com/certificate/UC-57e7751d-de00-4827-9c6f-cd27e761ca5f/',
  python: 'https://www.testdome.com/certificates/69256e0fa65342b998ba403bb6584d41',
}

const accents = {
  mathe: '#d6f26a',
  figata: '#c4b5fd',
  accountant: '#ffb088',
  orderoo: '#9fd0c8',
}

const hobbyImage = {
  music: '/hobbies/music.svg',
  cinema: '/hobbies/cinema.svg',
  football: '/hobbies/football.svg',
  travelling: '/hobbies/travelling.svg',
  chess: '/hobbies/chess.svg',
  bouldering: '/hobbies/bouldering.svg',
}

export const copies: Record<Locale, Copy> = {
  el: {
    ...contact,
    name: 'Αντώνης Σκαρλάτος',
    nameLines: ['Αντώνης', 'Σκαρλάτος'],
    eyebrow: 'Χαρτοφυλάκιο / 2026',
    place: 'Αθήνα',
    lede: 'Προγραμματιστής. Φυσικός στην εκπαίδευση, αναλυτής δεδομένων στην πράξη.',
    disciplines: 'Φυσική · Δεδομένα · Web',
    viewProjects: 'Δες τα έργα',
    scroll: 'Κύλιση',
    skip: 'Μετάβαση στο περιεχόμενο',
    introLabel: 'Εισαγωγή',
    profile: [
      'Απόφοιτος Φυσικής με μεταπτυχιακό στην Επιστήμη των Υπολογιστών και ενδιαφέρον για τον προγραμματισμό, την επιστήμη των δεδομένων και την ανάπτυξη ιστοσελίδων.',
      'Επιλυτής προβλημάτων με προσοχή στη λεπτομέρεια, αναλυτική σκέψη και έμφαση στη μαθηματική προσέγγιση.',
      'Ευέλικτος και προσαρμόσιμος σε νέους ρόλους και δεξιότητες.',
      'Εργασία σε ερευνητικούς και βιομηχανικούς τομείς ως αναλυτής δεδομένων για 3 χρόνια.',
      'Τώρα εργάζομαι σαν Web Developer.',
    ],
    journeyTitle: 'Η πορεία',
    journeyLede: 'Από τη φυσική στο λογισμικό.',
    supervisorsLabel: 'Επιβλέποντες',
    languagesLabel: 'Γλώσσες',
    certificatesLabel: 'Πιστοποιητικά',
    education: [
      {
        dates: '2015–2020',
        credential: 'Πτυχίο Φυσικής',
        school: 'ΕΚΠΑ, Αθήνα',
        detail: 'Τμήμα Φυσικής',
        thesisLabel: 'Πτυχιακή εργασία',
        thesis: 'Ανάλυση δεδομένων σε δίκτυα κινητών επικοινωνιών 5ης γενιάς',
        supervisors: 'Δρ. Άννα Τζανακάκη, Μάρκος Αναστασόπουλος',
      },
      {
        dates: '2020–2022',
        credential: 'Μεταπτυχιακός τίτλος σπουδών: Control and Computing',
        school: 'ΕΚΠΑ, Αθήνα',
        detail: 'Τμήμα Φυσικής, Τμήμα Πληροφορικής και Τηλεπικοινωνιών',
        thesisLabel: 'Διπλωματική εργασία',
        thesis: 'Ανάλυση της κινητικότητας των χρηστών σε συστήματα κινητών επικοινωνιών',
        thesisHref: pergamos,
        supervisors: 'Δρ. Άννα Τζανακάκη, Μάρκος Αναστασόπουλος',
      },
    ],
    work: [
      {
        dates: '02/2025–τώρα',
        role: 'Web Developer',
        place: 'FactSet',
        points: [
          'Εργασία και εκπαίδευση με σύγχρονες τεχνολογίες που χρησιμοποιούνται σε project πελατών όπως Vue.js, Typescript, E2E testing.',
          'Ανάπτυξη της ηλεκτρονικής ιστοσελίδας για μεγάλη επενδυτική τράπεζα στην Γερμανία. Διατήρηση κώδικα, προσθήκη λειτουργιών, εκτέλεση testing στον κώδικα.',
        ],
      },
      {
        dates: '01/2023–08/2024',
        role: 'Μηχανικός Ανάλυσης Δεδομένων',
        place: 'Performance Technologies, Αθήνα',
        points: [
          'Επίσημη εκπαίδευση και εξάσκηση σε Tableau, PowerBI, Vertica, MS SQL Server, PostgreSQL, XMLs, Git Version Control, Linux.',
          'Ενασχόληση με έργα που ανήκουν στην πυραμίδα Data Engineering. Συλλογή, μετασχηματισμός, καθαρισμός δεδομένων, χρήση εργαλείων ανάλυσης (κυρίως με χρήση Python) και οπτικοποίησή τους (Tableau, PowerBI).',
        ],
      },
      {
        dates: '11/2021–04/2022',
        role: 'Ερευνητής Ανάλυσης Δεδομένων',
        place: 'ΙΕΣΕ, Ινστιτούτο Επιταχυνώμενων Συστημάτων και Εφαρμογών, Αθήνα',
        points: [
          'Συνεργασία με τον καθηγητή μου στο πανεπιστήμιο σε έργα ανάλυσης δεδομένων για την κυκλοφορία των αυτοκινήτων και τις δονήσεις των σιδηροδρομικών γραμμών στην Ελλάδα.',
          'Συγκέντρωση, καθαρισμός και προεπεξεργασία δεδομένων για τον κατάλληλο χειρισμό.',
          'Αξιοποίηση μαθηματικών τεχνικών για την ανάπτυξη επιστημονικών λύσεων.',
          'Παρουσίαση προφορικώς και γραπτώς των ευρημάτων με προηγμένα μαθηματικά μοντέλα σε ξένους συναδέλφους από άλλα ευρωπαϊκά πανεπιστήμια.',
        ],
      },
      {
        dates: '11/2020–08/2021',
        role: 'Βοηθός Ερευνητής',
        place: 'ΙΕΣΕ, Ινστιτούτο Επιταχυνώμενων Συστημάτων και Εφαρμογών, Αθήνα',
        points: [
          'Συνεργασία με τον καθηγητή μου στο πανεπιστήμιο σε έργα ανάλυσης δεδομένων για προβλήματα τηλεπικοινωνιών.',
          'Συγκέντρωση, οργάνωση και διόρθωση ερευνητικών δεδομένων χρησιμοποιώντας στατιστικά εργαλεία για τη δημιουργία αντιπροσωπευτικών γραφημάτων για παρουσιάσεις.',
          'Βελτιστοποίηση στις διαδικασίες για την τήρηση αυστηρών προθεσμιών σε πολλαπλά έργα.',
        ],
      },
    ],
    languages: [
      'Ελληνικά (Μητρική)',
      'Αγγλικά (Πτυχίο Proficiency, Michigan)',
      'Γερμανικά (B1, Βασική Επικοινωνία)',
    ],
    certificates: [
      { label: '12/2024 Udemy: Mastering TypeScript – 2024 Edition', href: certificates.typescript },
      { label: '11/2024 Udemy: The Web Developer Bootcamp 2024', href: certificates.bootcamp },
      { label: '03/2023 Udemy: Advanced SQL, The Ultimate Guide' },
      { label: '12/2022 TestDome: Python', href: certificates.python },
    ],
    skillsLabel: 'Δεξιότητες',
    workKicker: '03 — Επιλεγμένα έργα',
    workTitle: 'Ελεύθερα έργα.',
    workIntro: 'Ιστοσελίδες και εφαρμογές που έφτιαξα μόνος ή ως μέλος μιας μικρής ομάδας.',
    projects: [
      {
        id: 'mathe',
        name: 'Μάθε Παιδί μου Αρχαία',
        dates: '',
        stack: 'Vue, Nuxt',
        summary: 'Σύγχρονη εκπαιδευτική πλατφόρμα, χτισμένη με Vue και Nuxt.',
        href: 'https://github.com/skarla21/mathe-paidi-mou-archaia',
        accent: accents.mathe,
      },
      {
        id: 'figata',
        name: 'Figata Café',
        dates: '',
        stack: 'Next.js',
        summary:
          'Μια κομψή, mobile-friendly ιστοσελίδα για το Figata καφέ, ένα τοπικό μαγαζί, με έμφαση στην ατμόσφαιρα και τα προϊόντα του.',
        href: 'https://www.figata.gr/',
        accent: accents.figata,
      },
      {
        id: 'accountant',
        name: 'Ιστοσελίδα για λογιστή',
        dates: '',
        stack: 'Next.js, Tailwind CSS',
        summary: 'Μια σύγχρονη, πολύγλωσση ιστοσελίδα για επαγγελματία λογιστή, ανεπτυγμένη με Next.js και Tailwind CSS.',
        href: 'https://www.giorgosrissetis.gr/',
        accent: accents.accountant,
      },
      {
        id: 'orderoo',
        name: 'Orderoo',
        dates: '02/2026–τώρα',
        stack: 'React, Next.js',
        summary:
          'Μια γενική εφαρμογή παραγγελιών για κάθε είδους κατάστημα. Μέλος της ομάδας ανάπτυξης, σε μικρή ομάδα 3 ατόμων, σε περιβάλλον start-up.',
        accent: accents.orderoo,
      },
    ],
    beyondTitle: 'Πέρα από την οθόνη',
    hobbies: [
      { id: 'music', label: 'Μουσική', image: hobbyImage.music },
      { id: 'cinema', label: 'Σινεμά', image: hobbyImage.cinema },
      { id: 'football', label: 'Ποδόσφαιρο', image: hobbyImage.football },
      { id: 'travelling', label: 'Ταξίδια', image: hobbyImage.travelling },
      { id: 'chess', label: 'Σκάκι', image: hobbyImage.chess },
      { id: 'bouldering', label: 'Μπούλντερινγκ', image: hobbyImage.bouldering },
    ],
    contactKicker: '05 — Επικοινωνία',
    contactTitle: 'Ας επικοινωνήσουμε.',
    cvLabel: 'Λήψη βιογραφικού',
    cv: '/cv/antonis-skarlatos-el.pdf',
    address: 'Αθήνα, 16232',
    seoDescription: 'Προγραμματιστής, αναλυτής δεδομένων και φυσικός στην Αθήνα.',
    nav: [
      { href: '#intro', label: 'Εισαγωγή' },
      { href: '#journey', label: 'Πορεία' },
      { href: '#work', label: 'Έργα' },
      { href: '#beyond', label: 'Ενδιαφέροντα' },
      { href: '#contact', label: 'Επικοινωνία' },
    ],
  },
  en: {
    ...contact,
    name: 'Antonis Skarlatos',
    nameLines: ['Antonis', 'Skarlatos'],
    eyebrow: 'Portfolio / 2026',
    place: 'Athens',
    lede: 'Web developer. Physicist by training, data by practice.',
    disciplines: 'Physics · Data · Web',
    viewProjects: 'View projects',
    scroll: 'Scroll',
    skip: 'Skip to content',
    introLabel: 'Introduction',
    profile: [
      'A Physics graduate with a MSc in Computer Science and an interest in programming, data science and web development.',
      'Problem-solver with attention to detail, analytical thinking and an emphasis on mathematical approach.',
      'Flexible and adaptable to new roles and skills.',
      'Worked in research and industry fields as a data analyst and programmer for 3 years.',
      'Currently working as a Web Developer!',
    ],
    journeyTitle: 'The journey',
    journeyLede: 'From physics to software.',
    supervisorsLabel: 'Supervisors',
    languagesLabel: 'Languages',
    certificatesLabel: 'Certificates',
    education: [
      {
        dates: '2015–2020',
        credential: 'Bachelor of Science: Physics',
        school: 'National and Kapodistrian University of Athens',
        detail: 'Department of Physics',
        thesisLabel: 'Thesis',
        thesis: 'Data Analytics in 5th Generation Mobile Communication Networks',
        supervisors: 'Anna Tzanakaki, Markos Anastasopoulos',
      },
      {
        dates: '2020–2022',
        credential: 'Master of Science: Control and Computing',
        school: 'National and Kapodistrian University of Athens',
        detail: 'Department of Physics, Department of Informatics and Telecommunications',
        thesisLabel: 'Thesis',
        thesis: 'User mobility analysis in mobile communication systems',
        thesisHref: pergamos,
        supervisors: 'Anna Tzanakaki, Markos Anastasopoulos',
      },
    ],
    work: [
      {
        dates: '02/2025–now',
        role: 'Web Developer',
        place: 'FactSet',
        points: [
          'Working with technologies used in client projects, like Vue.js, Typescript, E2E testing.',
          'Developing the web application for a big investment bank in Germany. Maintaining code, adding features, performing tests in the code.',
        ],
      },
      {
        dates: '01/2023–08/2024',
        role: 'Data Analytics Engineer',
        place: 'Performance Technologies, Athens',
        points: [
          'Official training and practicing on Tableau, PowerBI, Vertica, MS SQL Server, PostgreSQL, XMLs, Git version control, Linux.',
          'Engagement with projects belonging in the Data Engineering pyramid. Collecting, transforming, cleaning data, using analytics tools (mainly with Python scripts) and visualizing them (Tableau, PowerBI).',
        ],
      },
      {
        dates: '11/2021–04/2022',
        role: 'Data Research Analyst',
        place: 'IASA, Institute of Accelerating Systems and Applications, Athens',
        points: [
          'Collaboration with my university professor on data analytics projects for car traffic and train track vibrations for the largest train company in Greece.',
          'Compiled, cleaned and pre-processed data for proper handling.',
          'Leveraged mathematical techniques to develop engineering and scientific solutions.',
          'Presented findings orally and in writing with advanced mathematical models to foreign colleagues from other European Universities.',
        ],
      },
      {
        dates: '11/2020–08/2021',
        role: 'Research Associate',
        place: 'IASA, Institute of Accelerating Systems and Applications, Athens',
        points: [
          'Collaborated with my university professor on data analytics projects for telecommunication problems.',
          'Gathered, arranged and corrected research data using statistical tools to create representative graphs for presentations.',
          'Streamlined research processes to meet tight deadlines for multiple projects.',
        ],
      },
    ],
    languages: [
      'Greek (Native Speaker)',
      'English (Certificate of Proficiency, Michigan)',
      'German (B1, Basic Communication)',
    ],
    certificates: [
      { label: '12/2024 Udemy: Mastering TypeScript – 2024 Edition', href: certificates.typescript },
      { label: '11/2024 Udemy: The Web Developer Bootcamp 2024', href: certificates.bootcamp },
      { label: '03/2023 Udemy: Advanced SQL, The Ultimate Guide' },
      { label: '12/2022 TestDome: Python', href: certificates.python },
    ],
    skillsLabel: 'Skills',
    workKicker: '03 — Selected work',
    workTitle: 'Freelance work.',
    workIntro: 'Sites and applications built alone, or as part of a small team.',
    projects: [
      {
        id: 'mathe',
        name: 'Mathe Paidi Mou Archaia',
        dates: '',
        stack: 'Vue, Nuxt',
        summary: 'A modern educational platform, built with Vue and Nuxt.',
        href: 'https://github.com/skarla21/mathe-paidi-mou-archaia',
        accent: accents.mathe,
      },
      {
        id: 'figata',
        name: 'Figata Café',
        dates: '',
        stack: 'Next.js',
        summary:
          'A modern, responsive website for Figata Café, a local café showcasing its atmosphere, products, and unique charm. Built with Next.js.',
        href: 'https://www.figata.gr/',
        accent: accents.figata,
      },
      {
        id: 'accountant',
        name: 'Accountant site',
        dates: '',
        stack: 'Next.js, Tailwind CSS',
        summary: 'A modern, multilingual website for an accounting professional, built with Next.js and Tailwind CSS.',
        href: 'https://www.giorgosrissetis.gr/',
        accent: accents.accountant,
      },
      {
        id: 'orderoo',
        name: 'Orderoo',
        dates: '02/2026–now',
        stack: 'React, Next.js',
        summary:
          'A white label ordering application for all kinds of stores. Working with a small team of 3 people in a start-up environment to develop this application. Built with React and Next.js.',
        accent: accents.orderoo,
      },
    ],
    beyondTitle: 'Beyond the screen',
    hobbies: [
      { id: 'music', label: 'Music', image: hobbyImage.music },
      { id: 'cinema', label: 'Cinema', image: hobbyImage.cinema },
      { id: 'football', label: 'Football', image: hobbyImage.football },
      { id: 'travelling', label: 'Travelling', image: hobbyImage.travelling },
      { id: 'chess', label: 'Chess', image: hobbyImage.chess },
      { id: 'bouldering', label: 'Bouldering', image: hobbyImage.bouldering },
    ],
    contactKicker: '05 — Contact',
    contactTitle: "Let's connect.",
    cvLabel: 'Download the CV',
    cv: '/cv/antonis-skarlatos-en.pdf',
    address: 'Athens, 16232',
    seoDescription: 'Web developer, data scientist, and physicist in Athens.',
    nav: [
      { href: '#intro', label: 'Intro' },
      { href: '#journey', label: 'Journey' },
      { href: '#work', label: 'Work' },
      { href: '#beyond', label: 'Beyond' },
      { href: '#contact', label: 'Contact' },
    ],
  },
}
