--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: sqlnlmatch; Type: SCHEMA; Schema: -; Owner: kjhong
--

CREATE SCHEMA sqlnlmatch;


ALTER SCHEMA sqlnlmatch OWNER TO kjhong;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alignments; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.alignments (
    sql_id integer,
    sql_idx integer,
    sentence_id integer,
    sentence_idx integer
);


ALTER TABLE sqlnlmatch.alignments OWNER TO kjhong;

--
-- Name: experiment; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.experiment (
    sql_id integer,
    nl_id integer,
    feat1 double precision,
    feat2 double precision,
    feat3 double precision
);


ALTER TABLE sqlnlmatch.experiment OWNER TO kjhong;

--
-- Name: nl_features0; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.nl_features0 (
    id integer NOT NULL,
    sentence_id integer,
    start_offset integer,
    end_offset integer,
    index integer,
    postag character varying(20),
    word character varying(150),
    lemma character varying(150)
);


ALTER TABLE sqlnlmatch.nl_features0 OWNER TO kjhong;

--
-- Name: nl_features0_id_seq; Type: SEQUENCE; Schema: sqlnlmatch; Owner: kjhong
--

CREATE SEQUENCE sqlnlmatch.nl_features0_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sqlnlmatch.nl_features0_id_seq OWNER TO kjhong;

--
-- Name: nl_features0_id_seq; Type: SEQUENCE OWNED BY; Schema: sqlnlmatch; Owner: kjhong
--

ALTER SEQUENCE sqlnlmatch.nl_features0_id_seq OWNED BY sqlnlmatch.nl_features0.id;


--
-- Name: nl_features1; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.nl_features1 (
    id integer NOT NULL,
    sentence_id integer,
    rel_name character varying(100),
    left_index integer,
    right_index integer
);


ALTER TABLE sqlnlmatch.nl_features1 OWNER TO kjhong;

--
-- Name: nl_features1_id_seq; Type: SEQUENCE; Schema: sqlnlmatch; Owner: kjhong
--

CREATE SEQUENCE sqlnlmatch.nl_features1_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sqlnlmatch.nl_features1_id_seq OWNER TO kjhong;

--
-- Name: nl_features1_id_seq; Type: SEQUENCE OWNED BY; Schema: sqlnlmatch; Owner: kjhong
--

ALTER SEQUENCE sqlnlmatch.nl_features1_id_seq OWNED BY sqlnlmatch.nl_features1.id;


--
-- Name: nl_features2; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.nl_features2 (
    sentence_id integer,
    indexes character varying(200),
    tag character varying(100)
);


ALTER TABLE sqlnlmatch.nl_features2 OWNER TO kjhong;

--
-- Name: sentences; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.sentences (
    id integer NOT NULL,
    url_id character varying(10),
    "position" integer,
    is_select boolean DEFAULT true,
    sentence text
);


ALTER TABLE sqlnlmatch.sentences OWNER TO kjhong;

--
-- Name: sentences_id_seq; Type: SEQUENCE; Schema: sqlnlmatch; Owner: kjhong
--

CREATE SEQUENCE sqlnlmatch.sentences_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sqlnlmatch.sentences_id_seq OWNER TO kjhong;

--
-- Name: sentences_id_seq; Type: SEQUENCE OWNED BY; Schema: sqlnlmatch; Owner: kjhong
--

ALTER SEQUENCE sqlnlmatch.sentences_id_seq OWNED BY sqlnlmatch.sentences.id;


--
-- Name: sql_features0; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.sql_features0 (
    id integer NOT NULL,
    sentence_id integer,
    start_offset integer,
    end_offset integer,
    index integer,
    postag character varying(20),
    word character varying(150),
    lemma character varying(150)
);


ALTER TABLE sqlnlmatch.sql_features0 OWNER TO kjhong;

--
-- Name: sql_features0_id_seq; Type: SEQUENCE; Schema: sqlnlmatch; Owner: kjhong
--

CREATE SEQUENCE sqlnlmatch.sql_features0_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sqlnlmatch.sql_features0_id_seq OWNER TO kjhong;

--
-- Name: sql_features0_id_seq; Type: SEQUENCE OWNED BY; Schema: sqlnlmatch; Owner: kjhong
--

ALTER SEQUENCE sqlnlmatch.sql_features0_id_seq OWNED BY sqlnlmatch.sql_features0.id;


--
-- Name: sql_features1; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.sql_features1 (
    id integer NOT NULL,
    sentence_id integer,
    rel_name character varying(100),
    left_index integer,
    right_index integer
);


ALTER TABLE sqlnlmatch.sql_features1 OWNER TO kjhong;

--
-- Name: sql_features1_id_seq; Type: SEQUENCE; Schema: sqlnlmatch; Owner: kjhong
--

CREATE SEQUENCE sqlnlmatch.sql_features1_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sqlnlmatch.sql_features1_id_seq OWNER TO kjhong;

--
-- Name: sql_features1_id_seq; Type: SEQUENCE OWNED BY; Schema: sqlnlmatch; Owner: kjhong
--

ALTER SEQUENCE sqlnlmatch.sql_features1_id_seq OWNED BY sqlnlmatch.sql_features1.id;


--
-- Name: sql_features2; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.sql_features2 (
    sentence_id integer,
    indexes character varying(200),
    tag character varying(100)
);


ALTER TABLE sqlnlmatch.sql_features2 OWNER TO kjhong;

--
-- Name: sqls; Type: TABLE; Schema: sqlnlmatch; Owner: kjhong; Tablespace: 
--

CREATE TABLE sqlnlmatch.sqls (
    id integer NOT NULL,
    sentence_id integer,
    is_valid boolean DEFAULT true,
    sql text
);


ALTER TABLE sqlnlmatch.sqls OWNER TO kjhong;

--
-- Name: sqls_id_seq; Type: SEQUENCE; Schema: sqlnlmatch; Owner: kjhong
--

CREATE SEQUENCE sqlnlmatch.sqls_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sqlnlmatch.sqls_id_seq OWNER TO kjhong;

--
-- Name: sqls_id_seq; Type: SEQUENCE OWNED BY; Schema: sqlnlmatch; Owner: kjhong
--

ALTER SEQUENCE sqlnlmatch.sqls_id_seq OWNED BY sqlnlmatch.sqls.id;


--
-- Name: id; Type: DEFAULT; Schema: sqlnlmatch; Owner: kjhong
--

ALTER TABLE ONLY sqlnlmatch.nl_features0 ALTER COLUMN id SET DEFAULT nextval('sqlnlmatch.nl_features0_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: sqlnlmatch; Owner: kjhong
--

ALTER TABLE ONLY sqlnlmatch.nl_features1 ALTER COLUMN id SET DEFAULT nextval('sqlnlmatch.nl_features1_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: sqlnlmatch; Owner: kjhong
--

ALTER TABLE ONLY sqlnlmatch.sentences ALTER COLUMN id SET DEFAULT nextval('sqlnlmatch.sentences_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: sqlnlmatch; Owner: kjhong
--

ALTER TABLE ONLY sqlnlmatch.sql_features0 ALTER COLUMN id SET DEFAULT nextval('sqlnlmatch.sql_features0_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: sqlnlmatch; Owner: kjhong
--

ALTER TABLE ONLY sqlnlmatch.sql_features1 ALTER COLUMN id SET DEFAULT nextval('sqlnlmatch.sql_features1_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: sqlnlmatch; Owner: kjhong
--

ALTER TABLE ONLY sqlnlmatch.sqls ALTER COLUMN id SET DEFAULT nextval('sqlnlmatch.sqls_id_seq'::regclass);

