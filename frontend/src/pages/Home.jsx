import PageHeader from "../components/PageHeader";
import StatCard from "../components/StatCard";
import Footer from "../components/Footer";

import "./Home.css";

function Home() {
    return (
        <div>

            <PageHeader
                title="LLM Defense Dashboard"
                subtitle="Monitor attacks, defenses, logs and analytics in real time."
            />

            <div className="home-cards">

                <StatCard
                    title="Total Attacks"
                    value="0"
                />

                <StatCard
                    title="Blocked"
                    value="0"
                />

                <StatCard
                    title="Success Rate"
                    value="0%"
                />

                <StatCard
                    title="Average Risk"
                    value="0"
                />

            </div>

            <Footer />

        </div>
    );
}

export default Home;