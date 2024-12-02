#homesis
class css:
        #CSS to style a upload file button in change role in bank section
        css = '''
        <style>
            div[data-testid="column"]:has(>div>div>div>div[data-testid="element-container"] >div[data-testid='stFileUploader']) {
                width: max-content;
            }
            div[data-testid="column"]:has(>div>div>div>div[data-testid="element-container"] >div[data-testid='stFileUploader']) section {
                padding: 0;
                float: left;
            }
            div[data-testid="column"]:has(>div>div>div>div[data-testid="element-container"] >div[data-testid='stFileUploader']) section > input + div {
                display: none;
            }
            div[data-testid="column"]:has(>div>div>div>div[data-testid="element-container"] >div[data-testid='stFileUploader']) section + div {
                float: right;
                padding-top: 0;
            }

        </style>
         '''
        
        css_send_email_automation_hub = """
        <style>
            [data-testid='stFileUploader'] {
                width: max-content;
                color: blue;
     
            }
            [data-testid='stFileUploader'] section {
                padding: 0;
                float: left;
            }
            [data-testid='stFileUploader'] section > input + div {
                display: none;
            }
            [data-testid='stFileUploader'] section + div {
                float: left;
                padding-top: 0;
            }
            [data-testid='stFileUploaderFile'] {
                margin: 0;
                padding: 0;
                
            }



        </style>"""