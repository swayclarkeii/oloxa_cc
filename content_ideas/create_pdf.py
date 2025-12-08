#!/usr/bin/env python3
"""Generate PDF document about building the dictation service."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

def create_pdf():
    doc = SimpleDocTemplate(
        "/Users/swayclarke/coding_stuff/oloxa_cc/content_ideas/voice_dictation_build_idea.pdf",
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=HexColor('#2C3E50')
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=40,
        alignment=TA_CENTER,
        textColor=HexColor('#7F8C8D'),
        italic=True
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=HexColor('#2980B9')
    )

    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=13,
        spaceBefore=15,
        spaceAfter=8,
        textColor=HexColor('#16A085')
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=16
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leftIndent=20,
        rightIndent=20,
        backColor=HexColor('#F8F9FA'),
        borderPadding=10,
        leading=16
    )

    lesson_style = ParagraphStyle(
        'Lesson',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leftIndent=20,
        textColor=HexColor('#8E44AD'),
        italic=True,
        leading=16
    )

    story = []

    # Title
    story.append(Paragraph("Building a Voice Dictation System with AI", title_style))
    story.append(Paragraph("A Non-Technical Journey Through Unexpected Challenges", subtitle_style))

    # Introduction
    story.append(Paragraph("Introduction: The Vision", heading_style))
    story.append(Paragraph(
        "I wanted something simple: press a hotkey, speak my thoughts, and have clean, polished text "
        "appear wherever my cursor was. No more typing out long messages or prompts. Just speak naturally "
        "and let AI do the heavy lifting of transcription and cleanup.",
        body_style
    ))
    story.append(Paragraph(
        "What seemed like a straightforward project turned into an educational journey through the "
        "hidden complexities of how computers actually work. Here's what I learned building this system "
        "with the help of an AI assistant (Claude).",
        body_style
    ))

    # What We Built
    story.append(Paragraph("What We Built", heading_style))
    story.append(Paragraph(
        "The final system works like this:",
        body_style
    ))

    bullet_items = [
        "Press Control twice quickly to start recording",
        "Speak naturally into your microphone",
        "Press Control once to stop recording",
        "The system transcribes your speech using Whisper (an AI model that runs on your computer)",
        "The transcript is cleaned up using OpenAI's API (fixing grammar, removing filler words)",
        "The polished text automatically appears wherever your cursor is"
    ]

    for item in bullet_items:
        story.append(Paragraph(f"• {item}", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "It works in any application—text editors, browsers, chat apps, coding tools—anywhere you can type.",
        body_style
    ))

    # The Challenges
    story.append(Paragraph("The Unexpected Challenges", heading_style))

    # Challenge 1
    story.append(Paragraph("Challenge 1: 'It Works on My Machine' (But Which Machine?)", subheading_style))
    story.append(Paragraph(
        "One of the first hurdles was Python versions. My computer had multiple versions of Python installed "
        "(3.10, 3.12, 3.14), and they don't all work the same way. Some software packages only work with "
        "specific Python versions.",
        body_style
    ))
    story.append(Paragraph(
        "We initially tried using Python 3.14, the newest version, only to discover that a critical "
        "component (called 'numba') hadn't been updated to support it yet. The error message was cryptic: "
        "\"only versions >=3.10,<3.14 are supported.\"",
        body_style
    ))
    story.append(Paragraph(
        "Lesson learned: Newer isn't always better. Sometimes you need to use older, more stable "
        "versions of software because the ecosystem hasn't caught up yet.",
        lesson_style
    ))

    # Challenge 2
    story.append(Paragraph("Challenge 2: The Virtual Environment Maze", subheading_style))
    story.append(Paragraph(
        "Python has a concept called \"virtual environments\"—isolated spaces where you can install "
        "packages without affecting your whole computer. Think of it like having separate toolboxes "
        "for different projects.",
        body_style
    ))
    story.append(Paragraph(
        "We created a virtual environment, installed all our packages there, but the program couldn't "
        "find them. After much debugging, we discovered the virtual environment's Python was secretly "
        "pointing to a different Python installation (through something called a 'symlink'). It was "
        "like having a key that opens a different door than you expected.",
        body_style
    ))
    story.append(Paragraph(
        "The solution? We eventually installed packages system-wide, which isn't the 'proper' way "
        "but it worked. Sometimes pragmatism beats perfection.",
        lesson_style
    ))

    # Challenge 3
    story.append(Paragraph("Challenge 3: macOS Really Cares About Security", subheading_style))
    story.append(Paragraph(
        "Modern Macs are very protective about which programs can do what. Our dictation service needed "
        "two special permissions:",
        body_style
    ))
    story.append(Paragraph("• <b>Microphone access</b> - to record your voice", body_style))
    story.append(Paragraph("• <b>Accessibility access</b> - to detect keyboard presses and type text", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Getting these permissions was tricky. At one point, a permission dialog appeared and I "
        "accidentally clicked \"Don't ask again\" instead of \"OK\"—which meant I had to dig into "
        "System Settings to manually grant permission.",
        body_style
    ))
    story.append(Paragraph(
        "Always read permission dialogs carefully. That split-second decision can create "
        "hours of troubleshooting.",
        lesson_style
    ))

    # Challenge 4
    story.append(Paragraph("Challenge 4: Background Apps Are Second-Class Citizens", subheading_style))
    story.append(Paragraph(
        "I wanted the dictation service to start automatically when I logged in, running invisibly "
        "in the background. macOS has a feature called \"Launch Agents\" designed exactly for this.",
        body_style
    ))
    story.append(Paragraph(
        "But there's a catch: programs running as Launch Agents have different security restrictions. "
        "Even though I'd granted keyboard monitoring permission to Python, the Launch Agent version "
        "couldn't access the keyboard. The error was ominous: \"This process is not trusted!\"",
        body_style
    ))
    story.append(Paragraph(
        "We also tried creating an Automator app (Apple's tool for creating simple applications), "
        "but hit the same wall.",
        body_style
    ))
    story.append(Paragraph(
        "The workaround: Instead of a true background service, we added a line to the Terminal's "
        "startup file. Now the service starts whenever I open Terminal. Not as elegant, but it works.",
        lesson_style
    ))

    # Challenge 5
    story.append(Paragraph("Challenge 5: The Mysterious '[No input provided.]' Text", subheading_style))
    story.append(Paragraph(
        "Once everything was \"working,\" there was still a bug: every transcription had "
        "\"[No input provided.]\" stuck at the beginning. This wasn't coming from the speech "
        "recognition—it was coming from the AI cleanup step.",
        body_style
    ))
    story.append(Paragraph(
        "The cleaning prompt I provided had instructions for handling empty input, and the AI was "
        "including that placeholder text even when there was real input. We had to add code to "
        "specifically strip out this artifact.",
        body_style
    ))
    story.append(Paragraph(
        "AI systems can be literal-minded. If your instructions mention edge cases, the AI "
        "might include references to them in unexpected places.",
        lesson_style
    ))

    # Challenge 6
    story.append(Paragraph("Challenge 6: The Hotkey That Stopped Working", subheading_style))
    story.append(Paragraph(
        "Originally, we used Enter to stop recording. This worked fine when testing directly, but "
        "when running as a background process, Enter key presses weren't being detected consistently. "
        "The recording would start but couldn't be stopped.",
        body_style
    ))
    story.append(Paragraph(
        "The fix was to use the Control key for everything: double-tap to start, single-tap to stop. "
        "Control is a \"modifier\" key that's detected more reliably across different contexts.",
        body_style
    ))
    story.append(Paragraph(
        "When something works in testing but fails in production, the environment is usually "
        "different in ways you didn't expect.",
        lesson_style
    ))

    # Challenge 7
    story.append(Paragraph("Challenge 7: Zombie Processes and Duplicate Instances", subheading_style))
    story.append(Paragraph(
        "At one point, we discovered three copies of the dictation service running simultaneously. "
        "Each time we'd tested starting the service, we'd created another instance without properly "
        "stopping the previous one.",
        body_style
    ))
    story.append(Paragraph(
        "We added a check: before starting, the system looks for any already-running instances. "
        "If one exists, it doesn't start another. This prevents the \"zombie process\" problem.",
        body_style
    ))
    story.append(Paragraph(
        "Always clean up after yourself. Programs that don't properly shut down can accumulate "
        "and cause strange behavior.",
        lesson_style
    ))

    story.append(PageBreak())

    # What I Learned
    story.append(Paragraph("Key Takeaways for Non-Technical Builders", heading_style))

    story.append(Paragraph("1. Read Error Messages Carefully", subheading_style))
    story.append(Paragraph(
        "Error messages often look like gibberish, but they usually contain the exact information "
        "needed to fix the problem. Look for file paths, version numbers, and phrases like "
        "\"not found\" or \"permission denied.\"",
        body_style
    ))

    story.append(Paragraph("2. Permissions Are Everything on Modern Systems", subheading_style))
    story.append(Paragraph(
        "macOS, Windows, and Linux all have security systems that restrict what programs can do. "
        "If something \"should work\" but doesn't, permissions are often the culprit. Check "
        "System Settings > Privacy & Security on Mac.",
        body_style
    ))

    story.append(Paragraph("3. The 'Happy Path' Rarely Works First Time", subheading_style))
    story.append(Paragraph(
        "Documentation and tutorials show the ideal scenario. Real computers have different "
        "configurations, versions, and quirks. Expect to troubleshoot.",
        body_style
    ))

    story.append(Paragraph("4. Working with AI Assistants", subheading_style))
    story.append(Paragraph(
        "AI assistants like Claude can write code and solve problems, but they can't see your "
        "screen or know your exact setup. Be specific about error messages, share screenshots "
        "when possible, and describe exactly what you see versus what you expected.",
        body_style
    ))

    story.append(Paragraph("5. Sometimes the 'Wrong' Solution Is Right", subheading_style))
    story.append(Paragraph(
        "We broke several \"best practices\": installing packages system-wide instead of in a "
        "virtual environment, using Terminal startup instead of a proper Launch Agent. But the "
        "goal was a working system, not a textbook example. Pragmatism has its place.",
        body_style
    ))

    # Technical Summary
    story.append(Paragraph("Technical Components (For the Curious)", heading_style))
    story.append(Paragraph(
        "For those who want to understand what's actually happening under the hood:",
        body_style
    ))

    tech_items = [
        "<b>Whisper</b> - OpenAI's speech recognition model that runs locally on your computer. "
        "It converts audio to text without sending data to the cloud.",
        "<b>OpenAI API</b> - Cloud service that cleans up the transcript using GPT-4o-mini. "
        "This is the only part that requires internet.",
        "<b>pynput</b> - Python library that monitors keyboard events and can simulate typing.",
        "<b>sounddevice</b> - Records audio from your microphone.",
        "<b>.zshrc</b> - A configuration file that runs commands when you open Terminal."
    ]

    for item in tech_items:
        story.append(Paragraph(f"• {item}", body_style))

    # Conclusion
    story.append(Paragraph("Conclusion", heading_style))
    story.append(Paragraph(
        "Building this dictation system took several hours of troubleshooting—far longer than the "
        "\"simple script\" I initially imagined. But the result is genuinely useful: I can now "
        "dictate messages, write prompts, and compose text by speaking naturally.",
        body_style
    ))
    story.append(Paragraph(
        "More importantly, I learned how much complexity hides beneath the surface of \"simple\" "
        "software. Every app on your computer navigates these same challenges: permissions, "
        "versions, environments, and platform quirks. The next time an app asks for a permission "
        "or an update breaks something, I'll have a better appreciation for why.",
        body_style
    ))
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "Built with the help of Claude (Anthropic's AI assistant) in November 2025.",
        subtitle_style
    ))

    doc.build(story)
    print("PDF created successfully!")

if __name__ == "__main__":
    create_pdf()
