create database syndeo;
use syndeo; 

CREATE TABLE users (
    uid VARCHAR(55) NOT NULL PRIMARY KEY,
    fullName VARCHAR(200) NOT NULL,
    email VARCHAR(90) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    dateOfBirth DATE NOT NULL,
    batch INT NOT NULL,
    department VARCHAR(60) NOT NULL,
    isMentor TINYINT NOT NULL,
    mobile VARCHAR(15) NOT NULL,
    contactPref VARCHAR(60) NOT NULL,
    postalCode INT NOT NULL,
    country VARCHAR(32) NOT NULL,
    linkedInURL VARCHAR(64) NOT NULL,
    resumeLink TEXT,
    summary TEXT NOT NULL,
    areasOfInterest TEXT NOT NULL,
    languages VARCHAR(30) NOT NULL,
    higherEd VARCHAR(100) DEFAULT NULL,
    licensesAndCerts TEXT DEFAULT NULL,
    isActive TINYINT NOT NULL DEFAULT 0,
    isAdmin TINYINT NOT NULL DEFAULT 0,
    tags VARCHAR(40) NOT NULL,
    profilePic BLOB 
);

CREATE TABLE allocations(
allocationId VARCHAR(55) NOT NULL PRIMARY KEY,
mentorUid VARCHAR(55) NOT NULL,
menteeUid VARCHAR(55) NOT NULL,
dateAllocated DATE NOT NULL,
isValidated TINYINT NOT NULL DEFAULT 0,
isAgreed TINYINT NOT NULL DEFAULT 0,
validator TEXT(40) NOT NULL
);

CREATE TABLE tags(
uid VARCHAR(55) NOT NULL PRIMARY KEY,
tag1 VARCHAR(55), tag2 VARCHAR(55),
tag3 VARCHAR(55), tag4 VARCHAR(55),
tag5 VARCHAR(55), tag6 VARCHAR(55),
tag7 VARCHAR(55),tag8 VARCHAR(55), 
tag9 VARCHAR(55),tag10 VARCHAR(55), 
tag11 VARCHAR(55), tag12 VARCHAR(55), 
tag13 VARCHAR(55),tag14 VARCHAR(55), 
tag15 VARCHAR(55),tag16 VARCHAR(55), 
tag17 VARCHAR(55), tag18 VARCHAR(55), 
tag19 VARCHAR(55), tag20 VARCHAR(55),
FOREIGN KEY (uid) REFERENCES users (uid)
);

