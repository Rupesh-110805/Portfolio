# replit.md

## Overview

This is a personal developer portfolio website built as a full-stack TypeScript application. It showcases projects, skills, and provides a contact form for visitors to send messages. The application features a modern dark-themed UI with smooth animations and scroll-based navigation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Routing**: Wouter for lightweight client-side routing
- **Styling**: Tailwind CSS with custom dark theme configuration and CSS variables for theming
- **UI Components**: shadcn/ui component library (New York style) built on Radix UI primitives
- **Animations**: Framer Motion for page transitions and scroll reveal effects
- **Smooth Scrolling**: react-scroll for navigation link scrolling
- **State Management**: TanStack React Query for server state management
- **Forms**: React Hook Form with Zod validation via @hookform/resolvers
- **Fonts**: Inter (sans-serif) and JetBrains Mono (monospace)

### Backend Architecture
- **Runtime**: Node.js with Express 5
- **Language**: TypeScript compiled with tsx for development, esbuild for production
- **API Design**: RESTful endpoints defined in `shared/routes.ts` with Zod schemas for type-safe request/response handling
- **Database ORM**: Drizzle ORM with PostgreSQL dialect
- **Build System**: Vite for frontend bundling, custom esbuild script for server bundling

### Data Storage
- **Database**: PostgreSQL (configured via DATABASE_URL environment variable)
- **Schema Location**: `shared/schema.ts` using Drizzle's pgTable definitions
- **Tables**:
  - `projects`: Portfolio projects with title, description, tech stack, links, and images
  - `skills`: Developer skills categorized by type (Languages, Frameworks, Tools)
  - `messages`: Contact form submissions with name, email, and message

### Code Organization
- **`client/`**: React frontend application
  - `src/components/`: Reusable UI components including shadcn/ui primitives
  - `src/pages/`: Page components (Home, NotFound)
  - `src/hooks/`: Custom React hooks for data fetching (projects, skills, messages)
  - `src/lib/`: Utility functions and query client configuration
- **`server/`**: Express backend
  - `index.ts`: Server entry point with middleware setup
  - `routes.ts`: API route handlers
  - `storage.ts`: Database access layer implementing IStorage interface
  - `db.ts`: Drizzle database connection
  - `vite.ts`: Vite dev server integration
  - `static.ts`: Production static file serving
- **`shared/`**: Code shared between frontend and backend
  - `schema.ts`: Drizzle table definitions and Zod schemas
  - `routes.ts`: API route definitions with type-safe contracts

### Development vs Production
- **Development**: Uses Vite dev server with HMR, integrated with Express via middleware
- **Production**: Frontend built to `dist/public`, server bundled to `dist/index.cjs` with selective dependency bundling for faster cold starts

## External Dependencies

### Database
- PostgreSQL database (connection via `DATABASE_URL` environment variable)
- Drizzle Kit for schema migrations (`npm run db:push`)

### UI/Component Libraries
- Radix UI primitives for accessible component foundations
- Lucide React for icons
- Embla Carousel for carousel functionality
- Vaul for drawer components
- cmdk for command palette functionality

### Build & Development Tools
- Vite with React plugin and Replit-specific plugins (runtime error overlay, cartographer, dev banner)
- esbuild for server bundling
- PostCSS with Tailwind CSS and Autoprefixer

### Form & Validation
- Zod for schema validation (shared between client and server)
- drizzle-zod for generating Zod schemas from Drizzle tables