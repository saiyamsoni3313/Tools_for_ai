# Tools API

![Tools API Logo](https://mewow.dev/static/logo.png)

## Overview

Welcome to the **Tools API** project! This repository contains the source code and configuration for a set of powerful and versatile APIs designed to empower AI agents with various advanced tools. Built using FastAPI, this project ensures high performance, scalability, and ease of use.

## Features

- **Get YouTube Transcription**: Extracts and transcribes audio from YouTube videos, providing accurate text transcriptions with precise timestamps.
- **Create Mermaid Diagram**: Generates professional-quality Mermaid diagrams from Markmap code, simplifying the creation of flowcharts and sequence diagrams.
- **Create PlantUML Diagram**: Transforms PlantUML code into detailed and visually appealing diagrams, perfect for visualizing complex systems.
- **Create Matplotlib Image**: Converts Python code into high-resolution Matplotlib diagrams, ideal for data visualization and reporting.
- **Create Seaborn Image**: Generates stunning Seaborn diagrams from Python code, helping create aesthetically pleasing and informative charts.
- **Create WordCloud**: Creates visually engaging word clouds from text data, summarizing large amounts of text effectively.
- **Create Apexcharts**: Produces interactive and customizable Apexcharts based on provided configurations, suitable for dynamic and responsive charts.
- **Create Graphviz Diagram**: Generates Graphviz diagrams from Markmap code, enabling the creation of complex network graphs and structured diagrams.
- **Create QuickChart**: Creates QuickChart images from various parameters, offering rapid and reliable charting solutions.
- **Read Webpage**: Converts a webpage to Markdown and can also summarize the page, simplifying web content extraction and formatting.
- **Deep Read Webpage**: Navigates links within a webpage, extracting and summarizing information from all linked pages for comprehensive web data retrieval.
- **Search Web**: Executes search queries across multiple search engines, returning comprehensive results and summarizing the content.

## Getting Started

### Prerequisites

- Python 3.10

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/tools-api.git
    cd tools-api
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the FastAPI server:

    ```sh
    uvicorn server:app --host 0.0.0.0 --port 8000 --workers -1
    ```

### Using Docker

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/tools-api.git
    cd tools-api
    ```

2. Build and start the services using Docker Compose:

    ```sh
    docker-compose up --build
    ```

3. The API will be accessible at `http://localhost:8000`.

### Environment Variables

Create a `.env` file in the root directory of the project with the following variables:

```env
token=
URL=
SEARCH_ENGINE_URL=
SEARCH_ENGINE_USERNAME=
SEARCH_ENGINE_PASSWORD=
USER_AGENT=
```

### API Documentation

The API documentation is available via OpenAPI at `http://localhost:8000/docs`.

## Contributing

We welcome contributions! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to get involved.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

Thank you to the FastAPI community for their support and contributions to this project.

---

For any questions or issues, please open an issue on GitHub.
Happy coding!
