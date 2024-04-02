# vyaparAI-backend

## Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine using Git:

```bash
git clone https://github.com/Pradyogik/vyaparAI-backend.git
cd vyaparAI-backend
```
### 2. Create a Virtual Environment

Create a virtual environment to manage your project's dependencies:

```bash

# For Unix/macOS
python3 -m venv venv

# For Windows
python -m venv venv
```
Activate the virtual environment:

```bash

# For Unix/macOS
source venv/bin/activate

# For Windows
.\venv\Scripts\activate
```
### 3. Install Requirements

Install the project dependencies using pip:

```bash

pip install -r requirements.txt
```
### 4. Create a .env File

Create a .env file in the root directory of your project and add the necessary environment variables in the following format:

.env
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```
Make sure to replace your_openai_api_key_here and your_serpapi_api_key_here with your actual API keys.
### 5. Run the Application

Start the FastAPI application with the following command:

```bash

uvicorn main:app --reload
```
The application will be available at http://127.0.0.1:8000.
## Testing the Application
Using curl

Test the application using curl with the following command:

```bash

curl -X 'POST' \
  'http://127.0.0.1:8000/process/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Name of the product : intitle:kala namak rice"}'
```
Using Axios in React

To make a POST request from a React application using Axios, follow this structure:

```bash
import axios from 'axios';

const postData = async () => {
  const response = await axios.post('http://127.0.0.1:8000/process/', {
    prompt: 'Name of the product : intitle:kala namak rice'
  });
  console.log(response.data);
};

postData();
```
# vyaparAI-backend
