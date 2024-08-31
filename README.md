![Showcase of zoltraakui](https://github.com/user-attachments/assets/8e06fa72-8e9b-4c7e-8eae-8b3d009765ea)

# Web User Interface for Zoltraak

Boost Your Creativity with Zoltraak

zoltraakui is a Streamlit-based user interface for the ZoltraakKlein project generator.

With a short request, you can generate various digital contents including code, images, audio, video, and more. The types covers business documents, multimedia contents like books, presentations with speech, web pages, and more.

Access to an instance is here: [https://zoltraak.app/](https://zoltraak.app/)

See old document in Japanese [README_JA.md](https://github.com/Habatakurikei/zoltraakui/blob/main/README_JA.md).

## Features

- Select what you want to create from multiple compiler options categorized by type
- Input project requirements as a short sentence instead of writing a long prompt, and generate project structures
- View generated outputs including code, images, audio, video, and more
- Download generated project files as a zip archive

This app is a part of Zoltraak project. See full list of features in [Zoltraak Klein](https://github.com/Habatakurikei/zoltraakklein).

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Habatakurikei/zoltraakui.git
   cd zoltraakui
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install streamlit==1.38.0 zoltraakklein
   ```

## Usage

![Main Screen of zoltraakui](https://github.com/user-attachments/assets/6f0ef7a1-cd12-4712-af37-4a71a234b6d5)

1. Run the Streamlit app:
   ```
   streamlit run main.py
   ```
2. Open your web browser and navigate to the provided URL (usually `http://localhost:8501`)
3. Select a compiler category and specific compiler from the sidebar
4. Input your request on a pop-up window
5. Generate the initial project structure includeing name and requirements definition
6. Optionally perform domain expansions to generate more digital contents based on the requirements definition
7. View and download the generated outputs

## Project Structure

- `main.py`: The main Streamlit application entry point
- `ui_body.py`: Functions for rendering the main content of the UI
- `ui_sidebar.py`: Functions for rendering the sidebar content
- `ui_tabs.py`: Functions for rendering various output tabs in showcase
- `utils.py`: Utility functions for project generation and management
- `config.py`: Configuration settings

## Dependencies

- Python 3.9+
- Streamlit 1.38.0+
- ZoltraakKlein 1.0.6+

## Contributing

Any contributions are welcome.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
