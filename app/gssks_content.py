"""Idempotent, evidence-led programme and event content for the GSSKS public site."""
from datetime import date

from .extensions import db
from .models import Event, Project, ProjectBrief


EVENTS = [
    {
        "title": "Child Rights and Legal Awareness Interaction",
        "event_date": date(2023, 5, 16),
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """A child-rights and legal-awareness interaction was recorded during an inspection visit by an officer associated with the District Legal Services Authority. The session created an opportunity to discuss children's rights, protection, access to support and the role of the child-protection system.

The interaction formed part of GSSKS's wider effort to connect children in the Open Shelter Home with information, guidance and appropriate institutional support. It also reflected the importance of coordination between care settings and statutory child-protection stakeholders.

Programme focus: child-rights awareness, legal literacy, institutional interaction and protection-oriented guidance.

The interaction took place on 16 May 2023.""",
    },
    {
        "title": "World Environment Day – Learning Through Nature",
        "event_date": date(2023, 6, 5),
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """Children marked World Environment Day through a nature-focused learning activity that included planting trees and discussing the importance of the environment. The activity encouraged children to connect environmental awareness with everyday responsibility and care for shared spaces.

The programme used participation and practical learning to introduce environmental stewardship in an accessible way. Children were encouraged to observe nature, understand why green spaces matter and take part in a collective activity.

Programme focus: environmental awareness, tree planting, participation and learning through action.

The activity is recorded for 5 June 2023.""",
    },
    {
        "title": "Educational Visit to Rani Kamalapati Palace",
        "event_date": date(2023, 7, 19),
        "location": "Rani Kamalapati Palace, Bhopal, Madhya Pradesh",
        "description": """GSSKS organised an educational exposure visit to Rani Kamalapati Palace on 19 July 2023. The visit gave children an opportunity to learn beyond the classroom and engage with a local heritage site.

Educational visits help connect classroom learning with the history, culture and places of the city. The outing also provided a shared recreational experience and encouraged curiosity, observation and peer participation.

Programme focus: educational exposure, local heritage, experiential learning and recreation.""",
    },
    {
        "title": "Independence Day Celebration",
        "event_date": date(2023, 8, 15),
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """Children at the Open Shelter Home took part in an Independence Day celebration. The programme provided a shared setting for children to participate in a national occasion, learn about its significance and express a sense of belonging.

National-day observances form part of the centre's cultural and recreational activities, alongside learning, sports and creative participation.

Programme focus: civic awareness, cultural participation, group activities and national-day learning.""",
    },
    {
        "title": "Gandhi Jayanti – Values and Community Learning",
        "event_date": date(2023, 10, 2),
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """GSSKS marked Gandhi Jayanti through a centre-based activity for children. The observance provided an opportunity to introduce values associated with the day, encourage discussion and create a shared learning experience.

The programme formed part of the centre's wider calendar of cultural, educational and recreational activities designed to support participation and personal development.

Programme focus: values-based learning, cultural awareness and child participation.""",
    },
    {
        "title": "Children's Day Celebration",
        "event_date": date(2023, 11, 14),
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """Children's Day was observed with activities that brought children together for participation, recreation and celebration. The centre's programme records also describe games, cultural activities and the distribution of learning materials and prizes during the reporting period.

The celebration placed children at the centre of the day and created space for enjoyment, confidence-building and positive interaction with peers and caregivers.

Programme focus: child participation, recreation, cultural activities and encouragement.""",
    },
    {
        "title": "Christmas Day Educational and Recreational Outing",
        "event_date": date(2023, 12, 25),
        "location": "People's Mall, Bhopal, Madhya Pradesh",
        "description": """Children took part in a Christmas Day outing to People's Mall on 25 December 2023. The visit offered a change of environment and an opportunity for recreation, shared experiences and learning outside the shelter setting.

Educational and recreational outings are part of the programme's broader approach to holistic development, helping children experience public spaces, participate in group activities and build positive memories in a safe, organised setting.

Programme focus: recreation, social participation, exposure and group learning.""",
    },
    {
        "title": "Gandhi Shilp Bazaar – Artisan Exhibition 2024",
        "event_date": date(2024, 9, 11),
        "location": "Urban Haat, Gauhar Mahal, Bhopal, Madhya Pradesh",
        "description": """Gyan Path Shiksha Evam Samaj Kalyan Samiti conducted the seven-day Gandhi Shilp Bazaar from 11 to 17 September 2024 at Urban Haat, Gauhar Mahal, Bhopal, under the MSS of the Ministry of Textiles, Government of India.

The exhibition brought together 50 artisans and presented a wide range of traditional products and crafts to the public. The displayed product range included jute products, Assam bamboo products, dry-stone work, handmade bedsheets, Madhubani paintings, silk sarees, jute and POP pottery, patchwork, zari work, paintings and woollen or fibre-yarn crafts.

The event created a public-facing platform for artisans to present their work, engage with visitors and generate sales. Reported sales during the seven-day programme exceeded ₹14,95,577.

Programme focus: artisan visibility, traditional craft promotion, market access and livelihood support.

Duration: 11–17 September 2024. The event listing uses the opening date; the programme ran for seven days.""",
    },
    {
        "title": "International Yoga Day – Wellbeing and Participation",
        "event_date": date(2024, 6, 21),
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """Children participated in an International Yoga Day activity as part of the centre's health, fitness and recreational programme. The observance introduced children to movement, physical wellbeing and the value of making time for healthy routines.

The activity complemented the programme's ongoing focus on health check-ups, nutrition, sports and physical fitness, while encouraging children to participate together.

Programme focus: physical wellbeing, healthy habits, participation and recreation.""",
    },
    {
        "title": "Diwali Celebration at the Open Shelter Home",
        "event_date": None,
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """Children celebrated Diwali at the Open Shelter Home through a centre-based cultural activity. The celebration formed part of the programme's annual calendar of festivals and shared occasions, creating an opportunity for children to participate in a familiar community celebration in a supportive setting.

Programme focus: cultural participation, belonging, recreation and shared celebration.

Programme period: 2024–25. The specific date of the centre celebration is not listed.""",
    },
    {
        "title": "Cleanliness and Safe-Surroundings Drive",
        "event_date": None,
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """Children took part in cleanliness activities within the shelter-home environment. The activity encouraged shared responsibility for maintaining clean, orderly and welcoming spaces and connected everyday habits with health and wellbeing.

Programme focus: hygiene awareness, responsibility, teamwork and care for shared surroundings.

Programme period: 2024–25. An individual event date is not listed.""",
    },
    {
        "title": "Creative Learning and Rangoli Activities",
        "event_date": None,
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """Creative activities including painting and rangoli gave children opportunities to express ideas, practise fine-motor skills and participate in group learning. These activities formed part of the centre's recreational and personality-development programme.

Programme focus: creativity, expression, participation and confidence-building.

Reporting period: 2024–25. The programme record does not specify an individual event date.""",
    },
    {
        "title": "Employment-Oriented and Vocational Skills Training",
        "event_date": None,
        "location": "GSSKS Open Shelter Home, Bhopal, Madhya Pradesh",
        "description": """The 2024–25 programme record includes employment-oriented training for children. This work sits within the shelter programme's broader skill-development approach, which describes basic computer training, exposure to crafts or trade skills, career guidance and pre-employment learning, particularly for adolescents.

The intention is to help young people build practical capabilities and become better prepared for future education, training and livelihood pathways.

Programme focus: practical skills, vocational exposure, career awareness and preparation for future opportunities.

Programme period: 2024–25. Specific training dates and course titles are not listed.""",
    },
    {
        "title": "Open Shelter Home Programme Highlights – 2022–23",
        "event_date": None,
        "location": "GSSKS Open Shelter Home units, Bhopal, Madhya Pradesh",
        "description": """The 2022–23 programme year brought together daily care, health support, learning and recreation for children attending GSSKS Open Shelter Home services.

Daily support included three meals, routine medical check-ups, first-aid availability, vaccination support, clothing and essential learning materials. Children took part in indoor and outdoor games, cultural activities and group recreation. Computer-based learning was also provided to strengthen digital familiarity and basic learning skills.

The programme included interaction and visits by child-welfare and government representatives, alongside the distribution of uniforms and books. These activities connected everyday care with educational participation, health and institutional engagement.

Programme areas: nutrition and daily care; health and first aid; vaccination; education and computer learning; clothing and stationery; recreation; and child-welfare coordination.

Reporting period: 2022–23.""",
    },
    {
        "title": "Open Shelter Home Programme Highlights – 2023–24",
        "event_date": None,
        "location": "GSSKS Open Shelter Home units, Bhopal, Madhya Pradesh",
        "description": """During 2023–24, GSSKS combined daily shelter-home care with educational exposure, national and cultural observances, health support and opportunities for children to participate in the community.

Activities included morning prayer, three healthy meals, routine medical check-ups, first aid, computer learning and annual examinations. Children participated in World Environment Day tree-planting activities, an educational visit to Rani Kamalapati Palace, Independence Day and Gandhi Jayanti observances, Children's Day activities and a Christmas outing to People's Mall. The programme also included an interaction with Child Welfare Committee representatives and a legal-awareness interaction during a visit by a District Legal Services Authority officer.

The year’s activities connected classroom learning with local heritage, civic awareness, environmental responsibility and positive group experiences.

Programme areas: daily care; education; health; environmental awareness; heritage exposure; national-day activities; child-rights awareness; recreation; and institutional coordination.

Reporting period: 2023–24.""",
    },
    {
        "title": "Open Shelter Home Programme Highlights – 2024–25",
        "event_date": None,
        "location": "GSSKS Open Shelter Home units, Bhopal, Madhya Pradesh",
        "description": """The 2024–25 programme year continued the combination of daily care, education, health, recreation and practical skill development across GSSKS Open Shelter Home activities.

Children received daily meals and routine medical check-ups and participated in computer classes, annual examinations and employment-oriented training. Creative activities included painting and rangoli. The programme also included International Yoga Day participation, Diwali celebrations, cleanliness activities, plantation, recreational outings and group activities. Visits and interactions included engagement with Special Juvenile Police Unit inspectors and a discussion with a clinical psychologist during a centre visit.

The activities supported physical wellbeing, creativity, practical learning, confidence and positive engagement with support professionals.

Programme areas: nutrition; health; digital learning; examinations; vocational exposure; creative activities; yoga and fitness; cleanliness; plantation; recreation; and professional interaction.

Reporting period: 2024–25.""",
    },
]


def seed_gssks_events():
    """Add verified programme entries once; never overwrite administrator edits."""
    created = 0
    for item in EVENTS:
        existing = Event.query.filter_by(title=item["title"]).first()
        if existing:
            continue
        db.session.add(Event(
            title=item["title"],
            event_date=item["event_date"],
            location=item["location"],
            description=item["description"],
            status="Completed",
            registration_enabled=False,
        ))
        created += 1
    if created:
        db.session.commit()

    # A complete project page for the verified 2024 artisan exhibition.
    project = Project.query.filter_by(slug="gandhi-shilp-bazaar-2024").first()
    if project is None:
        project = Project(
            title="Gandhi Shilp Bazaar 2024",
            slug="gandhi-shilp-bazaar-2024",
            category="Artisan & Livelihood Development",
            location="Urban Haat, Gauhar Mahal, Bhopal, Madhya Pradesh",
            status="Completed",
            short_description="A seven-day artisan exhibition connecting traditional crafts with public visibility and market access.",
            description="""Gyan Path Shiksha Evam Samaj Kalyan Samiti conducted Gandhi Shilp Bazaar from 11 to 17 September 2024 at Urban Haat, Gauhar Mahal, Bhopal, under the MSS of the Ministry of Textiles, Government of India.

The seven-day exhibition brought together 50 artisans and welcomed members of the general public. It presented a diverse range of handmade and traditional products, including jute products, Assam bamboo products, dry-stone work, handmade bedsheets, Madhubani paintings, silk sarees, jute and POP pottery, patchwork, zari work, paintings and woollen or fibre-yarn crafts.

The exhibition provided artisans with a shared platform to display their products, interact with visitors and generate sales. Reported sales during the programme exceeded ₹14,95,577.""",
            published=True,
            featured=False,
        )
        db.session.add(project)
        db.session.flush()

    brief = ProjectBrief.query.filter_by(project_id=project.id).first()
    if brief is None:
        brief = ProjectBrief(
            project_id=project.id,
            duration="11–17 September 2024 (seven days)",
            objective="Provide a public exhibition platform for artisans to showcase traditional products, engage with visitors and generate sales.",
            beneficiaries="50 participating artisans.",
            activities="Seven-day public exhibition at Urban Haat, Gauhar Mahal, Bhopal; display of jute, Assam bamboo, dry-stone, textile, painting, pottery, patchwork, zari and woollen/fibre-yarn crafts.",
            outcomes="Reported sales exceeded ₹14,95,577 during the seven-day programme. The exhibition increased public visibility for the participating artisans and their craft products.",
            partners="Conducted under the MSS of the Ministry of Textiles, Government of India.",
        )
        db.session.add(brief)
        db.session.commit()
    return created
