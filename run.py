from app import create_app, db
from app.models import Job, User
from werkzeug.security import generate_password_hash

app = create_app()

def seed_data():
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="hr@example.com").first():
            user = User(
                email="hr@example.com",
                name="HR Manager",
                phone="0555555555",
                address="Riyadh, Saudi Arabia",
                password=generate_password_hash("dummy123")
            )
            db.session.add(user)
            db.session.commit()

        if not Job.query.first():
            jobs = [
                Job(
                    title="Restaurant Manager",
                    company="Savory Bites Co.",
                    description="""
                    <br><h4>Lead Our Team to Success</h4>
                    <p>We're looking for an experienced Restaurant Manager to oversee daily operations, manage staff, and ensure exceptional customer service in a fast-paced dining environment. You’ll be instrumental in upholding brand standards and fostering a team-focused atmosphere.</p><br>
                    <ul>
                        <li>Manage inventory, vendor relationships, and supply orders</li>
                        <li>Maintain high food safety and sanitation standards</li>
                        <li>Recruit, train, and develop front and back-of-house staff</li>
                        <li>Ensure smooth daily operations and resolve customer issues effectively</li>
                        <li>Optimize scheduling and labor costs</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="Marketing Specialist",
                    company="BrightWave Media",
                    description="""
                    <br><h4>Drive Brand Awareness and Growth</h4>
                    <p>We're hiring a data-driven and creative Marketing Specialist to develop, execute, and monitor marketing campaigns across various platforms. The role requires a deep understanding of digital media, brand strategy, and analytics to help elevate our presence and drive revenue.</p><br>
                    <ul>
                        <li>Design and execute multichannel marketing campaigns</li>
                        <li>Create compelling content for social, email, and paid ads</li>
                        <li>Track KPIs and report on performance metrics</li>
                        <li>Work with cross-functional teams including product and sales</li>
                        <li>Maintain consistency with brand identity and messaging</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="Customer Service Representative",
                    company="ConnectPro Solutions",
                    description="""
                    <br><h4>Be the Voice of Our Company</h4>
                    <p>We are seeking a friendly and professional Customer Service Representative who can build trust with our clients and resolve issues with efficiency and empathy. You’ll handle support across email, chat, and phone to ensure high satisfaction and client retention.</p><br>
                    <ul>
                        <li>Handle inquiries, product support, and account updates</li>
                        <li>Utilize CRM software to document and resolve issues</li>
                        <li>Escalate technical issues as needed</li>
                        <li>Maintain service-level standards and response times</li>
                        <li>Contribute to knowledge base and FAQs</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="Logistics Coordinator",
                    company="Global Freight Corp.",
                    description="""
                    <br><h4>Optimize Our Supply Chain</h4>
                    <p>We're looking for a detail-oriented Logistics Coordinator to manage our supply chain operations and streamline processes for domestic and international shipping. This is a critical role for ensuring timely, cost-effective deliveries across the board.</p><br>
                    <ul>
                        <li>Coordinate shipment schedules with carriers and suppliers</li>
                        <li>Track delivery progress and resolve transit issues</li>
                        <li>Work with customs and documentation for international freight</li>
                        <li>Maintain accurate inventory and shipping records</li>
                        <li>Ensure compliance with safety and regulatory standards</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="Financial Analyst",
                    company="AlphaCore Investments",
                    description="""
                    <br><h4>Support Business Decisions with Data</h4>
                    <p>As a Financial Analyst, you’ll work closely with our leadership team to provide insight into business performance, evaluate opportunities, and guide financial strategy. Ideal for someone who enjoys making data tell a story.</p><br>
                    <ul>
                        <li>Develop financial models and forecasts</li>
                        <li>Conduct variance and profitability analysis</li>
                        <li>Assist with budgeting and strategic planning</li>
                        <li>Present actionable insights to executives</li>
                        <li>Monitor market trends and assess financial risk</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="Event Planner",
                    company="Blue Horizon Events",
                    description="""
                    <br><h4>Create Memorable Experiences</h4>
                    <p>Join our creative and driven event planning team! You'll be responsible for crafting unforgettable events for corporate clients, weddings, and galas. From initial concepts to on-site coordination, your attention to detail will shine.</p><br>
                    <ul>
                        <li>Manage full-cycle event planning and execution</li>
                        <li>Source and manage vendor relationships</li>
                        <li>Create event budgets and timelines</li>
                        <li>Ensure client satisfaction and adherence to vision</li>
                        <li>Coordinate staff and logistics on event day</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="UI/UX Designer",
                    company="PixelCrafters Studio",
                    description="""
                    <br><h4>Design Intuitive User Experiences</h4>
                    <p>We're seeking a creative UI/UX Designer to craft beautiful and functional user interfaces across web and mobile platforms. You'll collaborate closely with product managers and developers to translate user needs into elegant designs.</p><br>
                    <ul>
                        <li>Develop wireframes, prototypes, and high-fidelity mockups</li>
                        <li>Conduct user research and usability testing</li>
                        <li>Maintain and evolve the design system</li>
                        <li>Ensure responsive, accessible, and intuitive designs</li>
                        <li>Collaborate across teams to implement feedback quickly</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="DevOps Engineer",
                    company="NextGen CloudOps",
                    description="""
                    <br><h4>Streamline Our Infrastructure</h4>
                    <p>We're hiring a DevOps Engineer to build and maintain CI/CD pipelines, improve system reliability, and automate deployments across environments. This is a hands-on role ideal for someone passionate about performance and scalability.</p><br>
                    <ul>
                        <li>Implement infrastructure-as-code with tools like Terraform</li>
                        <li>Manage CI/CD pipelines and automate release processes</li>
                        <li>Monitor, troubleshoot, and improve system uptime</li>
                        <li>Collaborate with development and QA teams</li>
                        <li>Ensure security and compliance best practices</li>
                    </ul>
                    """,
                    posted_by=1
                ),
                Job(
                    title="Sales Executive",
                    company="VertexTech Solutions",
                    description="""
                    <br><h4>Drive Growth Through Relationships</h4>
                    <p>We're looking for a motivated Sales Executive to generate new business opportunities and build long-term client relationships. You’ll be working with cutting-edge software solutions and contributing directly to our growth targets.</p><br>
                    <ul>
                        <li>Identify and qualify leads through outreach and networking</li>
                        <li>Present tailored product demos and proposals</li>
                        <li>Negotiate contracts and close deals</li>
                        <li>Track and report on pipeline progress</li>
                        <li>Collaborate with marketing and customer success teams</li>
                    </ul>
                    """,
                    posted_by=1
                ),
            ]
            db.session.bulk_save_objects(jobs)
            db.session.commit()

seed_data()

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
