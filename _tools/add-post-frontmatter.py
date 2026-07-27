#!/usr/bin/env python3
import os

ROOT = "/Users/schacon/projects/scottchacon-site/src/posts"

# basename -> (image path, excerpt)
META = {
 "2024-10-19-on-using-flags-to-represent-languages.md": (
   "/assets/images/covers/flags.svg",
   "Why national flags remain the most universally recognizable way to represent languages in an interface — and where they fall short."),
 "2011-08-31-github-flow.md": (
   "/assets/images/covers/github-flow.svg",
   "Why we don't use git-flow at GitHub, and the simpler branch-and-deploy workflow we use instead."),
 "2011-07-11-reset.html": (
   "/assets/images/covers/reset.svg",
   "Demystifying git reset by following Git's three trees. This walkthrough later became part of the Pro Git book."),
 "2010-08-25-notes.markdown": (
   "/assets/images/covers/notes.svg",
   "Attaching extra data to a commit without changing its SHA, using the little-known git notes command."),
 "2010-06-09-pro-git-zh.markdown": (
   "/assets/images/covers/pro-git-zh.svg",
   "Pro Git is now available in a simplified Chinese translation, thanks to the tireless work of Chunzi."),
 "2010-06-06-pro-git-on-kindle.markdown": (
   "/assets/images/covers/pro-git-on-kindle.svg",
   "Pro Git is now available as a proper Kindle edition, downloadable straight from the Amazon store."),
 "2010-05-25-blog-over.markdown": (
   "/assets/images/covers/blog-over.svg",
   "Retiring my old blog that hopped from host to host and domain to domain over the years, for something new."),
 "2010-04-11-environment.markdown": (
   "/assets/images/covers/environment.svg",
   "A tour of the environment variables Git respects, and how they can quietly shape your workflow."),
 "2010-03-17-replace.markdown": (
   "/assets/images/covers/replace.svg",
   "Another hidden Git feature: using git replace to transparently swap one object in for another."),
 "2010-03-10-bundles.markdown": (
   "/assets/images/covers/bundles.svg",
   "Moving commits between repositories with no network at all, by packaging a push into a git bundle file."),
 "2010-03-08-rerere.markdown": (
   "/assets/images/covers/rerere.svg",
   "Teaching Git to remember how you resolved a conflict so it can replay that resolution next time — git rerere."),
 "2010-03-04-smart-http.markdown": (
   "/assets/images/covers/smart-http.svg",
   "The new Smart HTTP transport in Git, and how it makes cloning and fetching over plain HTTP fast."),
 "2010-03-02-undoing-merges.markdown": (
   "/assets/images/covers/undoing-merges.svg",
   "Kicking off a series of Git tips with the tricky business of undoing a merge that's already been committed."),
 "2009-12-17-this-year.markdown": (
   "/assets/images/covers/this-year.svg",
   "A year-end reflection, after mostly stepping away from blogging through 2009."),
 "2009-08-19-translate-this.markdown": (
   "/assets/images/covers/translate-this.svg",
   "Git makes forking and contributing easy — a call to help translate the Pro Git book into more languages."),
 "2009-07-28-the-gory-details.markdown": (
   "/assets/images/covers/the-gory-details.svg",
   "Overwhelmed by the response to Pro Git's launch — 10,000 visitors on day one — plus notes on what comes next."),
 "2009-02-19-do-what-you-want.markdown": (
   "/assets/images/covers/do-what-you-want.svg",
   "Reflections sparked by Chris Wanstrath's StartupRiot keynote on building a company by doing what you love."),
}

def yaml_escape(s):
    return '"' + s.replace('"', '\\"') + '"'

count = 0
for dirpath, _, files in os.walk(ROOT):
    for fn in files:
        if fn not in META:
            continue
        path = os.path.join(dirpath, fn)
        with open(path) as f:
            text = f.read()
        img, exc = META[fn]
        lines = text.split("\n")
        # find the second '---' (end of frontmatter)
        idxs = [i for i, l in enumerate(lines) if l.strip() == "---"]
        assert len(idxs) >= 2, path
        end = idxs[1]
        assert "image:" not in text[:text.find("\n", text.find("---")+3)+ (idxs[1]*0)] or True
        inject = [f"image: {img}", f"excerpt: {yaml_escape(exc)}"]
        new_lines = lines[:end] + inject + lines[end:]
        with open(path, "w") as f:
            f.write("\n".join(new_lines))
        count += 1
        print("updated", fn)
print("total:", count)
