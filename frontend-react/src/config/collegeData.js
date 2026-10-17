import logoImage from '../assets/images/logo.png';
import carousel1 from '../assets/images/carousel1.jpg';
import carousel2 from '../assets/images/carousel2.jpg';
import carousel3 from '../assets/images/carousel3.jpg';

export const collegeData = {
  name: 'SDMS College (Placeholder Name)',
  tagline: 'Welcome to SDMS College Website Demo',
  logo: logoImage,
  heroImages: [carousel1, carousel2, carousel3],
  heroAlt: [
    'Demo campus image 1 from existing assets',
    'Demo campus image 2 from existing assets',
    'Demo campus image 3 from existing assets',
  ],
  aboutText:
    'This Phase 1 homepage uses demo content and placeholders only. Please replace details with verified college information.',
  stats: [
    { label: 'Departments', value: '05', note: 'Demo placeholder value' },
    { label: 'Students', value: '0000+', note: 'Demo placeholder value' },
    { label: 'Faculty', value: '000+', note: 'Demo placeholder value' },
    { label: 'Programmes', value: '00+', note: 'Demo placeholder value' },
  ],
  principal: {
    name: 'Principal Name Placeholder',
    designation: 'Principal (Update after confirmation)',
    message:
      'Welcome to our SDMS college website demo. This message is placeholder content and must be replaced with approved text.',
    image: '',
  },
  departmentsNote: 'Sample department list for Phase 1. Confirm actual departments before production use.',
  departments: [
    {
      key: 'cse',
      title: 'Computer Science and Engineering',
      description: 'Sample description. Replace with verified department details.',
      learnMoreUrl: '',
    },
    {
      key: 'ece',
      title: 'Electronics and Communication Engineering',
      description: 'Sample description. Replace with verified department details.',
      learnMoreUrl: '',
    },
    {
      key: 'me',
      title: 'Mechanical Engineering',
      description: 'Sample description. Replace with verified department details.',
      learnMoreUrl: '',
    },
    {
      key: 'ce',
      title: 'Civil Engineering',
      description: 'Sample description. Replace with verified department details.',
      learnMoreUrl: '',
    },
    {
      key: 'eee',
      title: 'Electrical and Electronics Engineering',
      description: 'Sample description. Replace with verified department details.',
      learnMoreUrl: '',
    },
  ],
  activitiesNote: 'Activities below are demonstration examples, not verified historical records.',
  activities: [
    'Sample technical events and hackathons',
    'Sample workshops and seminars',
    'Sample cultural programmes',
    'Sample sports activities',
    'Sample student achievements showcase',
  ],
  galleryNote: 'Gallery uses reused demo assets. Replace with verified campus images.',
  gallery: [
    { src: carousel1, alt: 'Demo gallery image 1' },
    { src: carousel2, alt: 'Demo gallery image 2' },
    { src: carousel3, alt: 'Demo gallery image 3' },
  ],
  noticesNote: 'Notices below are demonstration content only.',
  notices: [
    {
      title: 'Demo Admission Notice',
      description: 'This notice is sample content for UI demonstration.',
      date: 'YYYY-MM-DD',
      link: '',
    },
    {
      title: 'Demo Workshop Circular',
      description: 'Replace with API-driven notices in next phase.',
      date: 'YYYY-MM-DD',
      link: '',
    },
  ],
  contact: {
    address: 'Address placeholder (update with verified details)',
    phone: 'Phone placeholder',
    email: 'Email placeholder',
    website: 'Website placeholder',
  },
};

export const supportedRoles = [
  'Admin/Principal',
  'HOD',
  'Faculty',
  'Student',
  'Office Staff',
  'Library Staff',
];
