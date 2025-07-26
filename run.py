from datetime import datetime, timedelta
from app import create_app, db
from app.models import Job, User
from werkzeug.security import generate_password_hash

app = create_app()

def seed_data():
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="admin@Careerly.com").first():
            user = User(
                email="admin@Careerly.com",
                name="Nasser Mohammed",
                phone="05399997502",
                address="Riyadh, Saudi Arabia",
                bio=None,           # optional, can omit or set a string
                experience=None,    # optional
                education=None,     # optional
                skills=None,        # optional, comma-separated string like "Python, Flask"
                password=generate_password_hash("%2Bj^EIl$KE0(}984*)(#@)")
            )
            db.session.add(user)
            db.session.commit()


        if not Job.query.first():
            jobs = [
                Job(
                    title="Restaurant Manager",
                    company="Savory Bites Co.",
                    salary="$4,000 - $5,000",
                    job_type="Full-time",
                    location="Riyadh, Saudi Arabia",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "As the Restaurant Manager at Savory Bites Co., you will oversee all daily operations, "
                        "ensuring excellent customer service, staff management, and smooth workflow. "
                        "You will coordinate with kitchen staff, handle budgeting and inventory, and develop "
                        "strategies to boost sales and customer satisfaction. The ideal candidate has proven leadership skills, "
                        "strong organizational abilities, and experience in the food and beverage industry. "
                        "You will foster a positive work environment while maintaining compliance with health and safety standards."
                    ),
                    posted_by=1
                ),
                Job(
                    title="Marketing Specialist",
                    company="BrightWave Media",
                    salary="$3,500 - $4,500",
                    job_type="Full-time",
                    location="Jeddah, Saudi Arabia",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "BrightWave Media is seeking a creative and analytical Marketing Specialist to join our team. "
                        "You will design, implement, and optimize marketing campaigns across digital and traditional platforms. "
                        "Responsibilities include content creation, market research, performance tracking, and collaboration with sales teams. "
                        "A deep understanding of social media marketing, SEO, and data-driven decision-making is essential. "
                        "Join us to help shape compelling brand narratives and increase market reach."
                    ),
                    posted_by=1
                ),
                Job(
                    title="Customer Service Representative",
                    company="ConnectPro Solutions",
                    salary="$2,800 - $3,200",
                    job_type="Part-time",
                    location="Remote",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "Join ConnectPro Solutions as a Customer Service Representative and provide top-tier support to our diverse client base. "
                        "This role requires excellent communication skills, empathy, and problem-solving ability to handle inquiries, complaints, and feedback effectively. "
                        "You will engage with customers through multiple channels including phone, email, and live chat, ensuring timely resolutions and a positive customer experience. "
                        "Flexible part-time hours allow for remote work in a dynamic and supportive environment."
                    ),
                    posted_by=1
                ),
                Job(
                    title="Logistics Coordinator",
                    company="Global Freight Corp.",
                    salary="$4,200 - $5,200",
                    job_type="Full-time",
                    location="Dammam, Saudi Arabia",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "Global Freight Corp. is looking for an organized and detail-oriented Logistics Coordinator to manage shipping schedules, "
                        "track inventory, and coordinate with carriers and warehouses. You will optimize transport routes, maintain compliance with regulations, "
                        "and troubleshoot logistical challenges to ensure timely delivery of goods. "
                        "Strong negotiation skills and proficiency with logistics software are required to succeed in this fast-paced role."
                    ),
                    posted_by=1
                ),
                Job(
                    title="Financial Analyst",
                    company="AlphaCore Investments",
                    salary="$5,000 - $6,500",
                    job_type="Full-time",
                    location="Riyadh, Saudi Arabia",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "AlphaCore Investments seeks a Financial Analyst to support investment decisions by conducting financial modeling, "
                        "analyzing market trends, and preparing detailed reports. "
                        "The successful candidate will work closely with portfolio managers and executives, providing actionable insights to optimize asset allocation. "
                        "Expertise in Excel, financial databases, and strong analytical skills are a must for this role."
                    ),
                    posted_by=1
                ),
                Job(
                    title="Event Planner",
                    company="Blue Horizon Events",
                    salary="$3,000 - $4,000",
                    job_type="Contract",
                    location="Jeddah, Saudi Arabia",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "Blue Horizon Events is seeking an Event Planner to organize and execute corporate and social events from conception to completion. "
                        "Responsibilities include vendor management, budgeting, scheduling, and client communication. "
                        "You will ensure every event runs smoothly, meets client expectations, and adheres to timelines and budgets. "
                        "This contract position demands excellent multitasking abilities and a passion for creativity."
                    ),
                    posted_by=1
                ),
                Job(
                    title="UI/UX Designer",
                    company="PixelCrafters Studio",
                    salary="$4,500 - $5,500",
                    job_type="Full-time",
                    location="Remote",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "PixelCrafters Studio is looking for a talented UI/UX Designer to create user-friendly digital experiences. "
                        "You will collaborate with developers and product managers to design wireframes, prototypes, and user interfaces that are both visually appealing and functional. "
                        "A strong portfolio demonstrating a deep understanding of user-centered design principles and proficiency with design tools is essential."
                    ),
                    posted_by=1
                ),
                Job(
                    title="DevOps Engineer",
                    company="NextGen CloudOps",
                    salary="$6,000 - $7,500",
                    job_type="Full-time",
                    location="Remote",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "NextGen CloudOps requires an experienced DevOps Engineer to automate infrastructure, monitor systems, "
                        "and collaborate across development teams to improve deployment pipelines. "
                        "You will be responsible for managing cloud environments, ensuring system reliability, and implementing CI/CD processes. "
                        "Expertise with Docker, Kubernetes, AWS/Azure, and scripting languages is highly desired."
                    ),
                    posted_by=1
                ),
                Job(
                    title="Sales Executive",
                    company="VertexTech Solutions",
                    salary="$4,000 - $6,000 + commission",
                    job_type="Full-time",
                    location="Riyadh, Saudi Arabia",
                    posted_date=datetime.utcnow(),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description=(
                        "VertexTech Solutions is seeking a motivated Sales Executive to drive revenue growth and build strong customer relationships. "
                        "You will identify new business opportunities, manage client accounts, and close deals with a focus on exceeding sales targets. "
                        "Excellent communication and negotiation skills, along with a results-driven mindset, are key to succeeding in this role."
                    ),
                    posted_by=1
                ),
            ]
            db.session.bulk_save_objects(jobs)
            db.session.commit()

seed_data()

if __name__ == "__main__":
    app.run(debug=False)
    app.run(host="0.0.0.0", port=5000)
