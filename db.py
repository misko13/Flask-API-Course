from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #creates sql object






#This Integrates SQLAlchemy with Flask. This handles setting up one or more engines, associating tables and models with specific engines,
# and cleaning up connections and sessions after each request.

#Only the engine configuration is specific to each application, other things like the model, table, metadata, and session
# are shared for all applications using that extension instance. Call init_app to configure the extension on an application.

# After creating the extension, create model classes by subclassing Model, and table classes with Table.
# These can be accessed before init_app is called, making it possible to define the models separately from the application.

# Accessing session and engine requires an active Flask applicationcontext. This includes methods like create_all which use the engine.