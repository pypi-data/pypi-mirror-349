from pathlib import Path
import typer
from jinja2 import Environment, FileSystemLoader

app = typer.Typer(help="Generate automation bot templates.")

@app.command()
def web_bot(name: str = typer.Option(None, "--name", help="Project name", prompt=True, hide_input=False),
            with_db: bool = typer.Option(False, "--with-db", help="Include DB connection setup in the generated project"),
            emailer: bool = typer.Option(False, help="Include emailer utility"),
            user: str = typer.Option(None, "--user", help="Database username"),
            password: str = typer.Option(None, "--password", help="Database password"),
            host: str = typer.Option(None, "--host", help="Database host"),
            service: str = typer.Option(None, "--service", help="Service name (e.g. ORCL)"),
            excel: bool = typer.Option(False, "--excel", help="Include Excel reader (pandas)", prompt=True),
            port: int = typer.Option(None, "--port", help="Port number")
            ):
    """
    Create a Web Automation Bot project scaffold.
    """
    # Setup paths
    base_dir = Path(name)
    assets_dir = base_dir / "assets"
    downloads_dir = base_dir / "downloads"
    logs_dir = base_dir / "logs"
    shared_dir = base_dir / "shared" 

    try:
        # Create directories
        assets_dir.mkdir(parents=True, exist_ok=True)
        downloads_dir.mkdir(parents=True, exist_ok=True)
        logs_dir.mkdir(parents=True, exist_ok=True)
        shared_dir.mkdir(parents=True, exist_ok=True)
        if with_db or emailer:
            shared_dir.mkdir(parents=True, exist_ok=True)
        

        # Setup Jinja2 environment
        template_path = Path(__file__).parent.parent / "templates"
        env = Environment(loader=FileSystemLoader(template_path))
        main_template = env.get_template("web_bot/web_bot.py.j2")
        ini_template = env.get_template("shared/app.ini.j2")
        logger_template = env.get_template("shared/logger.py.j2")
        print(excel)

        # Render templates
        class_name = name.replace("-", "_").title().replace("_", "")
        main_code = main_template.render(class_name=class_name, with_db=with_db, excel=excel, emailer=emailer)
        app_ini = ini_template.render(with_db=with_db, profile="DEFAULT", user=user, password=password, host=host, port=port, service=service)
        logger = logger_template.render(project_name=name)

        # Write rendered files
        (base_dir / "main.py").write_text(main_code)
        (assets_dir / "app.ini").write_text(app_ini)
        (shared_dir / "logger.py").write_text(logger)
        
        # Optional DB helper
        if with_db:
            db_template = env.get_template("shared/db_connection.py.j2")
            (shared_dir / "db_connections.py").write_text(db_template.render())  

        if emailer:
            email_template = env.get_template("shared/emailer.py.j2")
            (shared_dir / "emailer.py").write_text(email_template.render())   


        typer.echo(f"✅ Web Bot project '{name}' created successfully.")

    except Exception as e:
        typer.echo(f"❌ Error: {e}")


@app.command()
def recon_bot(name: str):
    """
    Create a Reconciliation Bot project.
    """
    typer.echo(f"Scaffolding recon-bot: {name}")
