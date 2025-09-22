const apiKey = "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";

const resumeText = `
Siva Sankar S P +91 8056027241 | sivasankarsp.24@gmail.com | Data Scientist | LinkedIn
Aspiring Data Scientist with expertise in machine learning, deep learning, NLP, and front-end development, skilled in Python, SQL, and Power BI.
Experienced in building high-accuracy sentiment analysis models, developing interactive dashboards, and delivering data-driven solutions through internships in Data Science, Front-End Development, and Quality Analysis.
Adept at combining analytical, technical, and problem-solving skills to create impactful AI-driven applications, with a strong passion for leveraging data to solve real-world challenges.

TECHNICAL SKILLS
Programming Languages: Python, SQL, HTML, CSS
Frameworks & Libraries: TensorFlow, Hugging Face Transformers, Scikit-learn, OpenCV, Matplotlib
Data & Visualization: Power BI, NetworkX
Testing & Tools: Manual Testing, Postman, Black-Box Testing, Regression
Project Management & Collaboration: Agile, Team Collaboration, Documentation
Soft Skills: Communication, Analytical Troubleshooting, Team Collaboration, Leadership

PROFESSIONAL EXPERIENCE
Quality Analyst Trainee (Intern) - Trsitha Global PVT LTD
Front-End Developer Intern - Salesqueen Software Solutions
Data Science Intern - Aristocrat Research IT Solutions

Projects:
- End-to-End Software Testing & Reporting with Tristha Global PVT LTD.
- Management Systems Development at Salesqueen Software Solutions.
- Structural Equation Modelling on FinTech Survey Data at Aristocrat Research IT Solutions.
- Sentiment Analysis on IMDb Dataset using DistilBERT.

CERTIFICATIONS
- Data Science – SoftLogic System
- Python for Data Science – IBM
- Machine Learning with Python – IBM
- Deep Learning with TensorFlow - IBM

EDUCATION
Panimalar Engineering College
B.E. in Electrical and Electronics Engineering
Chennai, TN Aug 2020 – May 2024
`;

async function getJarvisResponse(userMessage) {
  const url = 'https://openrouter.ai/api/v1/chat/completions';

  const body = {
    model: 'deepseek/deepseek-chat-v3.1',
    messages: [
      {
        role: 'system',
        content: `You are Jarvis AI, a personal assistant that only answers questions based on the following resume:\n${resumeText}`
      },
      {
        role: 'user',
        content: userMessage
      }
    ],
    stream: false,
  };

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    throw new Error(`OpenRouter API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example usage:
document.getElementById('sendBtn').addEventListener('click', async () => {
  const userInput = document.getElementById('userInput').value;
  if (!userInput.trim()) return;
  document.getElementById('chatArea').innerHTML += `<div><b>You:</b> ${userInput}</div>`;

  try {
    const jarvisReply = await getJarvisResponse(userInput);
    document.getElementById('chatArea').innerHTML += `<div><b>Jarvis:</b> ${jarvisReply}</div>`;
  } catch (error) {
    document.getElementById('chatArea').innerHTML += `<div style="color:red;"><b>Error:</b> ${error.message}</div>`;
  }
  document.getElementById('userInput').value = '';
});
