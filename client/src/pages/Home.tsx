import { motion } from "framer-motion";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { insertMessageSchema, type InsertMessage } from "@shared/schema";
import { useToast } from "@/hooks/use-toast";
import { Navigation } from "@/components/Navigation";
import { SectionHeading } from "@/components/SectionHeading";
import { ProjectCard } from "@/components/ProjectCard";
import { SocialLinks } from "@/components/SocialLinks";
import { useProjects } from "@/hooks/use-projects";
import { useSkills } from "@/hooks/use-skills";
import { useSendMessage } from "@/hooks/use-messages";
import { Loader2, ArrowRight } from "lucide-react";
import { Link as ScrollLink } from "react-scroll";

export default function Home() {
  const { data: projects, isLoading: projectsLoading } = useProjects();
  const { data: skills, isLoading: skillsLoading } = useSkills();
  const { mutateAsync: sendMessage, isPending: isSending } = useSendMessage();
  const { toast } = useToast();

  const form = useForm<InsertMessage>({
    resolver: zodResolver(insertMessageSchema),
    defaultValues: {
      name: "",
      email: "",
      message: "",
    },
  });

  const onSubmit = async (data: InsertMessage) => {
    try {
      await sendMessage(data);
      toast({
        title: "Message sent!",
        description: "Thanks for reaching out. I'll get back to you soon.",
      });
      form.reset();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to send message",
      });
    }
  };

  const groupedSkills = skills?.reduce((acc, skill) => {
    if (!acc[skill.category]) acc[skill.category] = [];
    acc[skill.category].push(skill);
    return acc;
  }, {} as Record<string, typeof skills>) || {};

  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary/20">
      <Navigation />

      {/* Left side fixed social links (desktop only) */}
      <div className="hidden lg:block fixed left-12 bottom-0 z-10 w-10">
        <SocialLinks vertical className="items-center" />
        <div className="w-px h-24 bg-border mx-auto mt-6" />
      </div>

      {/* Right side fixed email (desktop only) */}
      <div className="hidden lg:block fixed right-12 bottom-0 z-10 w-10">
        <div className="flex flex-col items-center gap-6">
          <a 
            href="mailto:hello@example.com" 
            className="text-mono text-sm text-muted-foreground hover:text-primary transition-colors writing-vertical-rl py-4"
            style={{ writingMode: 'vertical-rl' }}
          >
            hello@example.com
          </a>
          <div className="w-px h-24 bg-border" />
        </div>
      </div>

      <main className="container mx-auto px-6 md:px-12 lg:px-32">
        
        {/* HERO SECTION */}
        <section id="about" className="min-h-screen flex flex-col justify-center pt-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-primary font-mono mb-5 ml-1">Hi, my name is</p>
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-foreground mb-4">
              Jane Doe.
            </h1>
            <h2 className="text-4xl md:text-6xl font-bold tracking-tight text-muted-foreground mb-8">
              I build things for the web.
            </h2>
            <p className="max-w-xl text-muted-foreground text-lg leading-relaxed mb-12">
              I'm a computer science student and software engineer specializing in building (and occasionally designing) exceptional digital experiences. Currently, I'm focused on building accessible, human-centered products.
            </p>
            
            <ScrollLink
              to="projects"
              smooth={true}
              duration={500}
              className="inline-flex items-center justify-center px-8 py-4 border border-primary text-primary font-mono text-sm rounded hover:bg-primary/10 transition-colors cursor-pointer group"
            >
              Check out my work
              <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </ScrollLink>
          </motion.div>
        </section>

        {/* SKILLS SECTION */}
        <section id="skills" className="py-24 md:py-32 max-w-3xl mx-auto">
          <SectionHeading number="01" title="Skills & Technologies" />
          
          <div className="grid md:grid-cols-2 gap-12">
            <div className="space-y-6 text-muted-foreground leading-relaxed">
              <p>
                Hello! My name is Jane and I enjoy creating things that live on the internet. My interest in web development started back in 2012 when I decided to try editing custom Tumblr themes — turns out hacking together HTML & CSS is pretty fun!
              </p>
              <p>
                Fast-forward to today, and I’ve had the privilege of working at an advertising agency, a start-up, a huge corporation, and a student-led design studio.
              </p>
            </div>

            <div className="space-y-8">
              {skillsLoading ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
              ) : Object.keys(groupedSkills).length > 0 ? (
                Object.entries(groupedSkills).map(([category, items], idx) => (
                  <div key={category}>
                    <h3 className="text-lg font-bold text-foreground mb-3 font-mono border-l-2 border-primary pl-3">
                      {category}
                    </h3>
                    <ul className="grid grid-cols-2 gap-2">
                      {items.map((skill) => (
                        <li key={skill.id} className="flex items-center text-sm text-muted-foreground font-mono">
                          <span className="text-primary mr-2">▹</span>
                          {skill.name}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))
              ) : (
                <div className="text-muted-foreground text-sm font-mono italic">
                  No skills loaded yet.
                </div>
              )}
            </div>
          </div>
        </section>

        {/* PROJECTS SECTION */}
        <section id="projects" className="py-24 md:py-32">
          <SectionHeading number="02" title="Some Things I've Built" />
          
          {projectsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((n) => (
                <div key={n} className="h-96 bg-card rounded-lg animate-pulse border border-border" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 auto-rows-fr">
              {projects?.map((project, index) => (
                <ProjectCard key={project.id} project={project} index={index} />
              ))}
              {projects?.length === 0 && (
                <div className="col-span-full text-center py-20 text-muted-foreground font-mono">
                  Projects coming soon...
                </div>
              )}
            </div>
          )}
        </section>

        {/* CONTACT SECTION */}
        <section id="contact" className="py-24 md:py-32 max-w-2xl mx-auto text-center">
          <p className="text-primary font-mono mb-4">03. What's Next?</p>
          <h2 className="text-4xl md:text-5xl font-bold text-foreground mb-6">Get In Touch</h2>
          <p className="text-muted-foreground text-lg mb-12">
            Although I'm not currently looking for any new opportunities, my inbox is always open. Whether you have a question or just want to say hi, I'll try my best to get back to you!
          </p>

          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 max-w-md mx-auto text-left">
            <div className="space-y-2">
              <label htmlFor="name" className="text-sm font-mono text-muted-foreground">Name</label>
              <input
                id="name"
                {...form.register("name")}
                className="w-full bg-secondary/30 border border-border rounded p-3 text-foreground focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
                placeholder="John Doe"
              />
              {form.formState.errors.name && (
                <span className="text-destructive text-xs font-mono">{form.formState.errors.name.message}</span>
              )}
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-mono text-muted-foreground">Email</label>
              <input
                id="email"
                type="email"
                {...form.register("email")}
                className="w-full bg-secondary/30 border border-border rounded p-3 text-foreground focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
                placeholder="john@example.com"
              />
              {form.formState.errors.email && (
                <span className="text-destructive text-xs font-mono">{form.formState.errors.email.message}</span>
              )}
            </div>

            <div className="space-y-2">
              <label htmlFor="message" className="text-sm font-mono text-muted-foreground">Message</label>
              <textarea
                id="message"
                rows={4}
                {...form.register("message")}
                className="w-full bg-secondary/30 border border-border rounded p-3 text-foreground focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all resize-none"
                placeholder="Say hello..."
              />
              {form.formState.errors.message && (
                <span className="text-destructive text-xs font-mono">{form.formState.errors.message.message}</span>
              )}
            </div>

            <button
              type="submit"
              disabled={isSending}
              className="w-full mt-4 px-8 py-4 bg-transparent border border-primary text-primary font-mono text-sm rounded hover:bg-primary/10 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {isSending ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin" /> Sending...
                </span>
              ) : (
                "Send Message"
              )}
            </button>
          </form>
        </section>

        {/* Footer */}
        <footer className="py-8 text-center text-sm font-mono text-muted-foreground">
          <div className="lg:hidden mb-6 flex justify-center">
            <SocialLinks />
          </div>
          <p className="hover:text-primary transition-colors cursor-default">
            Built with React, TypeScript & Tailwind
          </p>
        </footer>
      </main>
    </div>
  );
}
