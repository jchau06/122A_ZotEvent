import mysql.connector


def get_connection():
    # returns a fresh MySQL connection whenever called.
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="cs122a"
    )


def setup_schema():
    # recreates the database schema from scratch.
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        database="cs122a"
    )
    cursor = conn.cursor()

    ddl_script = """
    DROP DATABASE IF EXISTS cs122a;
    CREATE DATABASE cs122a;
    USE cs122a;
    
    -- User Table
    CREATE TABLE User (
        uid INT,
        email VARCHAR(255) NOT NULL,
        username VARCHAR(255) NOT NULL,
        joined DATE NOT NULL,
        PRIMARY KEY (uid)
    );
    
    -- Organizer (Delta Table for ISA Relationship)
    CREATE TABLE Organizer (
        uid INT,
        department VARCHAR(255) NOT NULL,
        experience INT NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    );
    
    -- Participant (Delta Table for ISA Relationship)
    CREATE TABLE Participant (
        uid INT,
        type VARCHAR(255),
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    );
    
    -- Administrator (Delta Table for ISA Relationship)
    CREATE TABLE Administrator (
        uid INT,
        firstname VARCHAR(255) NOT NULL,
        lastname VARCHAR(255) NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
    );
    
    -- Event Table
    CREATE TABLE Event (
        eid INT,
        creator_uid INT NOT NULL,
        title VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        datetime DATETIME NOT NULL,
        PRIMARY KEY (eid),
        FOREIGN KEY (creator_uid) REFERENCES Organizer(uid) ON DELETE CASCADE
    );
    
    -- Slot Table (Weak Entity)
    CREATE TABLE Slot (
        eid INT,
        snum INT NOT NULL,
        is_reserved BOOLEAN NOT NULL,
        uid INT,
        PRIMARY KEY (eid, snum),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (uid) REFERENCES Participant(uid) ON DELETE SET NULL
    );
    
    -- Venue Table
    CREATE TABLE Venue (
        vid INT,
        street VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL,
        state VARCHAR(255) NOT NULL,
        zip VARCHAR(10) NOT NULL,
        PRIMARY KEY (vid)
    );
    
    -- OnCampus Table
    CREATE TABLE OnCampus (
        vid INT,
        code VARCHAR(255) NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    );
    
    -- OffCampus Table
    CREATE TABLE OffCampus (
        vid INT,
        distance INT NOT NULL,
        PRIMARY KEY (vid),
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    );
    
    -- Hosting Relation Table
    CREATE TABLE Hosting (
        eid INT NOT NULL,
        vid INT NOT NULL,
        is_primary BOOLEAN NOT NULL,
        PRIMARY KEY (eid, vid),
        FOREIGN KEY (eid) REFERENCES Event(eid) ON DELETE CASCADE,
        FOREIGN KEY (vid) REFERENCES Venue(vid) ON DELETE CASCADE
    );
    
    -- Approval Relation Table
    CREATE TABLE Approval (
        uid INT NOT NULL,
        vid INT NOT NULL,
        valid_from DATE NOT NULL,
        valid_until DATE NOT NULL,
        PRIMARY KEY (uid, vid),
        FOREIGN KEY (uid) REFERENCES Administrator(uid) ON DELETE CASCADE,
        FOREIGN KEY (vid) REFERENCES OffCampus(vid) ON DELETE CASCADE
    );
    """

    for statement in ddl_script.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)   
    conn.commit()
    cursor.close()
    conn.close()
