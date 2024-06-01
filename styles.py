chat_styles = """
        <style>
        .scrollable-table-container {
            max-height: 400px; /* Adjust the height as needed */
            overflow-y: auto; /* Enable vertical scrolling */
            overflow-x: auto; /* Enable horizontal scrolling for wide tables */
            display: block; /* Block display to ensure proper scrolling */
        }
        table {
            border-collapse: collapse;
            border-spacing: 0;
            width: 100%;
            border: 1px solid #ddd;
            border-radius: 12px; /* Smoother angles */
            overflow: hidden; /* Ensure border-radius works properly */
        }

        th, td {
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }

        th {
            background-color: #4e8af4; /* Cool blue color */
            color: white; /* Text color for the header */
        }

        .sql-code {
            background-color: #222; /* Dark background */
            color: white;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 20px;
        }
        </style>
        """


clear_button_style = """
        <style>.button-container {position: fixed; top: 10px; right: 10px;}</style>
        <div class="button-container">
            <button onclick="clearConversation()">🗑️</button>
        </div>
        """
