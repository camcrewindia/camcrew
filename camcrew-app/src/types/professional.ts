export interface ServiceItem {
  id: string;
  title: string;
  category: string;
  rate: number;
  unit: string;
  description: string;
}

export interface ReviewItem {
  id: string;
  clientName: string;
  clientAvatar?: string;
  rating: number;
  date: string;
  comment: string;
}

export interface ProfessionalProfile {
  id: string;
  userId: string;
  name: string;
  title: string;
  avatar: string;
  bannerImage: string;
  verified: boolean;
  rating: number;
  reviewCount: number;
  experienceYears: number;
  ratePerDay: number;
  bio: string;
  state: string;
  district: string;
  city: string;
  locations: string[];
  categories: string[];
  services: ServiceItem[];
  portfolio: string[];
  equipment: string[];
  certifications: string[];
  reviews: ReviewItem[];
  weeklyAvailability: { [day: string]: boolean };
  blockedDates: string[];
  iCalUrl?: string;
  socials?: {
    instagram?: string;
    website?: string;
    youtube?: string;
  };
  views?: number;
  totalEarnings?: number;
}
