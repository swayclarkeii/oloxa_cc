#!/usr/bin/env python3
"""Generate installation guide PDF"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from pathlib import Path

def create_pdf():
    script_dir = Path(__file__).parent.absolute()
    pdf_path = script_dir / "Installation_Guide.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
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
        fontSize=26,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=HexColor('#2C3E50'),
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=40,
        alignment=TA_CENTER,
        textColor=HexColor('#7F8C8D')
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=25,
        spaceAfter=12,
        textColor=HexColor('#2980B9'),
        fontName='Helvetica-Bold'
    )

    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=HexColor('#16A085'),
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=16
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Code'],
        fontSize=10,
        spaceAfter=12,
        leftIndent=20,
        fontName='Courier',
        backColor=HexColor('#F5F5F5'),
        borderPadding=10
    )

    note_style = ParagraphStyle(
        'Note',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        leftIndent=20,
        backColor=HexColor('#FFF9E6'),
        borderPadding=10,
        leading=16
    )

    story = []

    # Title Page
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Voice Dictation System", title_style))
    story.append(Paragraph("Installation Guide for macOS", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Transform your speech into polished text with AI", body_style))
    story.append(PageBreak())

    # Table of Contents
    story.append(Paragraph("Table of Contents", heading_style))
    story.append(Paragraph("1. What You're Installing", body_style))
    story.append(Paragraph("2. System Requirements", body_style))
    story.append(Paragraph("3. Installation Steps", body_style))
    story.append(Paragraph("4. Getting Your OpenAI API Key", body_style))
    story.append(Paragraph("5. Granting macOS Permissions", body_style))
    story.append(Paragraph("6. First Use", body_style))
    story.append(Paragraph("7. Troubleshooting", body_style))
    story.append(PageBreak())

    # Section 1
    story.append(Paragraph("1. What You're Installing", heading_style))
    story.append(Paragraph(
        "This dictation system lets you speak naturally and have your words appear as clean, "
        "polished text in any application on your Mac. It combines local speech recognition "
        "(Whisper) with cloud-based text cleaning (OpenAI) to give you the best results.",
        body_style
    ))
    story.append(Paragraph("<b>How it works:</b>", body_style))
    story.append(Paragraph("• Press Control twice quickly → Start recording", body_style))
    story.append(Paragraph("• Speak your message naturally", body_style))
    story.append(Paragraph("• Press Control once → Stop recording", body_style))
    story.append(Paragraph("• Text is transcribed, cleaned, and pasted automatically", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Works everywhere: Browsers, text editors, chat apps, code editors, anywhere you can type!",
        note_style
    ))

    # Section 2
    story.append(Paragraph("2. System Requirements", heading_style))
    story.append(Paragraph("<b>Operating System:</b> macOS 10.15 (Catalina) or newer", body_style))
    story.append(Paragraph("<b>Python:</b> Version 3.10, 3.11, 3.12, or 3.13", body_style))
    story.append(Paragraph("<b>OpenAI API Account:</b> Required for text cleaning (costs ~$0.01 per use)", body_style))
    story.append(Paragraph("<b>Microphone:</b> Built-in or external", body_style))
    story.append(Paragraph("<b>Disk Space:</b> About 1-2 GB for models and dependencies", body_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "NOTE: If you don't have Python installed, download it from python.org. "
        "The installer will check your Python version and guide you.",
        note_style
    ))

    # Section 3
    story.append(Paragraph("3. Installation Steps", heading_style))

    story.append(Paragraph("Step 1: Extract the ZIP File", subheading_style))
    story.append(Paragraph(
        "After downloading, double-click the ZIP file to extract it. You'll see a folder "
        "called 'voice-dictation-system' with several files inside.",
        body_style
    ))

    story.append(Paragraph("Step 2: Open Terminal", subheading_style))
    story.append(Paragraph("There are two ways to do this:", body_style))
    story.append(Paragraph(
        "<b>Easy way:</b> Right-click (or Control-click) on the folder and select "
        "'New Terminal at Folder'",
        body_style
    ))
    story.append(Paragraph(
        "<b>Manual way:</b> Open Terminal from Applications → Utilities → Terminal, "
        "then drag the folder into Terminal to get the path",
        body_style
    ))

    story.append(Paragraph("Step 3: Run the Installer", subheading_style))
    story.append(Paragraph("In Terminal, type this command and press Enter:", body_style))
    story.append(Paragraph("<code>bash install.sh</code>", code_style))
    story.append(Paragraph(
        "The installer will automatically:",
        body_style
    ))
    story.append(Paragraph("1. Check your Python installation", body_style))
    story.append(Paragraph("2. Install required packages (this takes 3-5 minutes)", body_style))
    story.append(Paragraph("3. Launch the setup wizard", body_style))

    story.append(Paragraph("Step 4: Follow the Setup Wizard", subheading_style))
    story.append(Paragraph(
        "The wizard will guide you through configuration. You'll need to provide your "
        "OpenAI API key (see next section for how to get one).",
        body_style
    ))

    story.append(PageBreak())

    # Section 4
    story.append(Paragraph("4. Getting Your OpenAI API Key", heading_style))
    story.append(Paragraph(
        "The dictation system uses OpenAI's GPT-4o-mini to clean up your transcripts. "
        "You need an API key for this:",
        body_style
    ))

    story.append(Paragraph("<b>Step 1:</b> Visit https://platform.openai.com/api-keys", body_style))
    story.append(Paragraph("<b>Step 2:</b> Sign in or create a free account", body_style))
    story.append(Paragraph("<b>Step 3:</b> Click the '+ Create new secret key' button", body_style))
    story.append(Paragraph("<b>Step 4:</b> Give it a name like 'Dictation System'", body_style))
    story.append(Paragraph("<b>Step 5:</b> Copy the key (it starts with 'sk-')", body_style))
    story.append(Paragraph("<b>Step 6:</b> Paste it when the setup wizard asks", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "IMPORTANT: Keep your API key private! Don't share it with anyone. "
        "It's like a password for your OpenAI account.",
        note_style
    ))

    story.append(Paragraph("About Costs:", subheading_style))
    story.append(Paragraph(
        "OpenAI charges based on usage. For this dictation system, costs are very low:",
        body_style
    ))
    story.append(Paragraph("• Typical cost: Less than $0.01 per dictation", body_style))
    story.append(Paragraph("• 100 dictations: Approximately $0.50-$1.00", body_style))
    story.append(Paragraph("• New accounts often get free credits to start", body_style))

    # Section 5
    story.append(PageBreak())
    story.append(Paragraph("5. Granting macOS Permissions", heading_style))
    story.append(Paragraph(
        "The first time you run the dictation service, macOS will ask for two permissions:",
        body_style
    ))

    story.append(Paragraph("Permission 1: Microphone Access", subheading_style))
    story.append(Paragraph(
        "A dialog will appear asking: '\"Python\" would like to access the microphone.'",
        body_style
    ))
    story.append(Paragraph("<b>Click 'OK'</b> to allow recording.", body_style))

    story.append(Paragraph("Permission 2: Accessibility Access", subheading_style))
    story.append(Paragraph(
        "A dialog will appear saying: 'This process is not trusted! Input event monitoring will not be possible...'",
        body_style
    ))
    story.append(Paragraph("Follow these steps:", body_style))
    story.append(Paragraph("1. Click 'Open System Settings' (or open manually)", body_style))
    story.append(Paragraph("2. Go to Privacy & Security → Accessibility", body_style))
    story.append(Paragraph("3. Click the lock icon to make changes (enter your password)", body_style))
    story.append(Paragraph("4. Find 'Terminal' or 'Python' in the list", body_style))
    story.append(Paragraph("5. Toggle the switch to ON", body_style))
    story.append(Paragraph("6. Close System Settings", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "TIP: If you accidentally click 'Don't Allow', you can grant permissions later "
        "in System Settings → Privacy & Security.",
        note_style
    ))

    # Section 6
    story.append(PageBreak())
    story.append(Paragraph("6. First Use", heading_style))

    story.append(Paragraph("Starting the Service", subheading_style))
    story.append(Paragraph("In Terminal, run:", body_style))
    story.append(Paragraph("<code>bash start_dictation.sh</code>", code_style))

    story.append(Paragraph(
        "You'll see the service loading (takes 10-20 seconds first time):",
        body_style
    ))
    story.append(Paragraph("<code>Loading Whisper model...</code>", code_style))
    story.append(Paragraph("<code>Whisper model 'base' loaded successfully</code>", code_style))
    story.append(Paragraph("<code>🎙️  Dictation Service Started</code>", code_style))

    story.append(Paragraph("Testing It Out", subheading_style))
    story.append(Paragraph("1. Open any app where you can type (Notes, browser, etc.)", body_style))
    story.append(Paragraph("2. Click in a text field", body_style))
    story.append(Paragraph("3. Press <b>Control</b> twice quickly (within 0.3 seconds)", body_style))
    story.append(Paragraph("4. You'll see a notification: 'Recording Started'", body_style))
    story.append(Paragraph("5. Speak your message clearly", body_style))
    story.append(Paragraph("6. Press <b>Control</b> once to stop", body_style))
    story.append(Paragraph("7. Watch the notifications:", body_style))
    story.append(Paragraph("   • 'Transcribing...'", body_style))
    story.append(Paragraph("   • 'Cleaning Text...'", body_style))
    story.append(Paragraph("   • 'Complete!'", body_style))
    story.append(Paragraph("8. Your cleaned text appears at the cursor!", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "TIP: The whole process takes 3-6 seconds. The notifications let you know it's working!",
        note_style
    ))

    # Section 7
    story.append(PageBreak())
    story.append(Paragraph("7. Troubleshooting", heading_style))

    story.append(Paragraph("Problem: 'No module named...' error", subheading_style))
    story.append(Paragraph("<b>Solution:</b> Run the installer again:", body_style))
    story.append(Paragraph("<code>bash install.sh</code>", code_style))

    story.append(Paragraph("Problem: Recording doesn't start", subheading_style))
    story.append(Paragraph("<b>Check:</b>", body_style))
    story.append(Paragraph("• Are you pressing Control twice quickly enough? (within 0.3 sec)", body_style))
    story.append(Paragraph("• Does Terminal/Python have Accessibility permission?", body_style))
    story.append(Paragraph("• Is the service running? You should see 'Dictation Service Started'", body_style))

    story.append(Paragraph("Problem: Text doesn't paste", subheading_style))
    story.append(Paragraph("<b>Solution:</b>", body_style))
    story.append(Paragraph("• Check Accessibility permissions in System Settings", body_style))
    story.append(Paragraph("• The system will copy to clipboard as fallback - try Cmd+V", body_style))

    story.append(Paragraph("Problem: 'API key not found' error", subheading_style))
    story.append(Paragraph("<b>Solution:</b> Run the setup wizard again:", body_style))
    story.append(Paragraph("<code>python3 setup_wizard.py</code>", code_style))

    story.append(Paragraph("Problem: Service is slow", subheading_style))
    story.append(Paragraph("<b>Normal behavior:</b> 3-6 seconds is expected", body_style))
    story.append(Paragraph("<b>To speed up:</b> Edit dictation_service.py, change line:", body_style))
    story.append(Paragraph("<code>WHISPER_MODEL_SIZE = \"tiny\"</code>", code_style))
    story.append(Paragraph("(Note: 'tiny' is faster but less accurate)", body_style))

    story.append(Paragraph("Problem: macOS update broke permissions", subheading_style))
    story.append(Paragraph("<b>Solution:</b> Re-grant permissions in System Settings", body_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Still having issues?", subheading_style))
    story.append(Paragraph("1. Make sure all permissions are granted", body_style))
    story.append(Paragraph("2. Try restarting Terminal", body_style))
    story.append(Paragraph("3. Check the README.md file for more details", body_style))

    # Footer
    story.append(PageBreak())
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(
        "You're all set! Enjoy hands-free dictation.",
        ParagraphStyle('Footer', parent=body_style, alignment=TA_CENTER, fontSize=14, textColor=HexColor('#7F8C8D'))
    ))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph(
        "For more information, see README.md",
        ParagraphStyle('Footer2', parent=body_style, alignment=TA_CENTER, fontSize=10, textColor=HexColor('#BDC3C7'))
    ))

    # Build PDF
    doc.build(story)
    print(f"✓ Installation guide created: {pdf_path}")

if __name__ == "__main__":
    create_pdf()
