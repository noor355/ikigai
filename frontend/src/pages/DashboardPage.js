import { useState } from "react";
import { useNavigate } from "react-router-dom";

function DashboardPage({ setToken }) {
  const navigate = useNavigate();
  
  // Track which step of the wizard we are on (1 to 4)
  const [step, setStep] = useState(1);
  
  // Store the user's answers
  const [answers, setAnswers] = useState({
    passion: "",
    profession: "",
    mission: "",
    vocation: ""
  });

 
  // Handle typing in the text boxes
  const handleChange = (field, value) => {
    setAnswers({ ...answers, [field]: value });
  };

  // Move to the next or previous step
  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  // Submit the final form to your AI backend (we will wire the API up next!)
  const handleSubmit = () => {
    console.log("Submitting these answers to the AI:", answers);
    alert("Answers submitted! Check the console.");
    // We will add the Axios call to your Python AI route here later
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif", maxWidth: "600px", margin: "0 auto" }}>
      
   
      

      {/* The Wizard Card */}
      <div style={{ backgroundColor: "#f8f9fa", padding: "30px", borderRadius: "8px", border: "1px solid #dee2e6", minHeight: "300px", display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
        
        {/* Progress Indicator */}
        <p style={{ color: "#6c757d", fontSize: "14px", margin: "0 0 20px 0" }}>Step {step} of 4</p>

        {/* Step 1: Passion */}
        {step === 1 && (
          <div>
            <h3>1. What do you love? (Passion)</h3>
            <p style={{ color: "#555" }}>Think about things that make you lose track of time. What are you deeply passionate about?</p>
            <textarea 
              rows="4" 
              style={{ width: "100%", padding: "10px", marginTop: "10px", borderRadius: "4px", border: "1px solid #ccc" }} 
              placeholder="I love to..."
              value={answers.passion}
              onChange={(e) => handleChange("passion", e.target.value)}
            />
          </div>
        )}

        {/* Step 2: Profession */}
        {step === 2 && (
          <div>
            <h3>2. What are you good at? (Profession)</h3>
            <p style={{ color: "#555" }}>List your skills, talents, and things people frequently ask you for help with.</p>
            <textarea 
              rows="4" 
              style={{ width: "100%", padding: "10px", marginTop: "10px", borderRadius: "4px", border: "1px solid #ccc" }} 
              placeholder="I am really good at..."
              value={answers.profession}
              onChange={(e) => handleChange("profession", e.target.value)}
            />
          </div>
        )}

        {/* Step 3: Mission */}
        {step === 3 && (
          <div>
            <h3>3. What does the world need? (Mission)</h3>
            <p style={{ color: "#555" }}>What problems do you care about solving in your community or the broader world?</p>
            <textarea 
              rows="4" 
              style={{ width: "100%", padding: "10px", marginTop: "10px", borderRadius: "4px", border: "1px solid #ccc" }} 
              placeholder="The world needs more..."
              value={answers.mission}
              onChange={(e) => handleChange("mission", e.target.value)}
            />
          </div>
        )}

        {/* Step 4: Vocation */}
        {step === 4 && (
          <div>
            <h3>4. What can you get paid for? (Vocation)</h3>
            <p style={{ color: "#555" }}>What services, products, or skills do you have that people are willing to pay for?</p>
            <textarea 
              rows="4" 
              style={{ width: "100%", padding: "10px", marginTop: "10px", borderRadius: "4px", border: "1px solid #ccc" }} 
              placeholder="People would pay me to..."
              value={answers.vocation}
              onChange={(e) => handleChange("vocation", e.target.value)}
            />
          </div>
        )}

        {/* Navigation Buttons */}
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: "30px" }}>
          {step > 1 ? (
            <button onClick={prevStep} style={{ padding: "10px 20px", backgroundColor: "#6c757d", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Back</button>
          ) : <div></div> /* Empty div to push the Next button to the right */}
          
          {step < 4 ? (
            <button onClick={nextStep} style={{ padding: "10px 20px", backgroundColor: "#007bff", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Next</button>
          ) : (
            <button onClick={handleSubmit} style={{ padding: "10px 20px", backgroundColor: "#28a745", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Submit to AI</button>
          )}
        </div>

      </div>
    </div>
  );
}

export default DashboardPage;