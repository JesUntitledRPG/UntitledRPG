## Supported Versions

Any versions prior to Rewrite 2 (PTB 1.0.0) should be considered unsafe. PTB 1.0.0 is technically unsafe, although technically safe to run if you don't get silly with what mods you load.

| Version       | Supported          |
| ------------- | ------------------ |
In Progress | ⏰
| PTB 1.0.1 | ⏰ |
Current Versions | ✔, ✅, ☑, ❌
| PTB 1.0.0 | ✔ |
| 0.5.xprealpha | ❌ |
| 0.4.xprealpha | ❌ |

✔  - Newest version

✅ - LTS version, usually a major release or the last minor or bugfix release of a version

☑  - Version is important to the community; may be patched

❌ - No support present, abandoned: use at your own risk

⏰ - It's literally an indev version of course it's going to be supported

## Reporting a Vulnerability

If the vulnerability is:
- present in versions prior to Rewrite 2 (PTB 1.0.0 Prealpha)
- is present in versions that haven't undergone certain recent/semirecent major changes
- present in versions that have no community presence and aren't new/seminew
- AND has been caused by my own code:
  
then;  
It won't be patched on those versions. Future versions will be patched, no doubt, but I recommend patching those yourself. If a good enough patch works, a release of that version with that vulnerability patched out may be released using a community patch, crediting those who worked on it on the credits through the Contributor List Guidelines.

If the vulnerability:
- has nothing to do with Untitled RPG Game, but with a library Untitled RPG Game uses, even if it's in an older version

then;
- Report to the library maintainers.
- Check if there are any branches of that library that have that vulnerability already patched out or a workaround for the vulnerability.
- Inform The Untitled Team of the vulnerability ASAP so those versions can be patched.

The libraries will be updated or the workarounds will be applied to versions with a checkmark. [Newest, LTS, Community Importance, Indev]

This also applies to Python's own vulnerabilities - if Untitled RPG Game can be affected by those, update the Python version and recompile the affected versions.
If the libraries can't be updated, please attempt to rewrite things that are vulnerable to said vulnerabilities.

If the vulnerability:
- is present in the latest version or indev releases
- allows for severe/high security vulnerations
- AND its cause is probably present in the codebase of Untitled RPG Game:

then;
All affected versions will be patched ASAP. Please report those vulnerabilities, as well as steps on how to reproduce them, to The Untitled Team as soon as possible through any standard form of communication.
