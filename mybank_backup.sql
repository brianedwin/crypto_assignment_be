--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.15 (Ubuntu 14.15-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: user_mybank
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO user_mybank;

--
-- Name: transactions; Type: TABLE; Schema: public; Owner: user_mybank
--

CREATE TABLE public.transactions (
    id integer NOT NULL,
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    amount_encrypted character varying NOT NULL,
    transaction_type character varying NOT NULL,
    created_at timestamp without time zone,
    signature character varying
);


ALTER TABLE public.transactions OWNER TO user_mybank;

--
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: user_mybank
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transactions_id_seq OWNER TO user_mybank;

--
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_mybank
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user_mybank
--

CREATE TABLE public.users (
    id integer NOT NULL,
    full_name character varying NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    id_number character varying NOT NULL,
    role character varying NOT NULL,
    otp_secret character varying,
    is_verified boolean,
    balance numeric(18,2) DEFAULT '0'::double precision NOT NULL
);


ALTER TABLE public.users OWNER TO user_mybank;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: user_mybank
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO user_mybank;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user_mybank
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: user_mybank
--

COPY public.alembic_version (version_num) FROM stdin;
7d0e9f559226
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: user_mybank
--

COPY public.transactions (id, sender_id, receiver_id, amount_encrypted, transaction_type, created_at, signature) FROM stdin;
7	5	6	8Jo0m+r05gXQ/xrMT1dyII8sZDC4GHlXJ0TbHSZ+vKrhjTGvskg6OnvbFpiadb3h	transfer	2025-03-01 22:27:18.609	979e0a59cb03f432303f2c5e589cbed414c8e54398a4dc48d163c914827099cb
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user_mybank
--

COPY public.users (id, full_name, username, password, id_number, role, otp_secret, is_verified, balance) FROM stdin;
2	Super Admin	admin	$2b$12$vc70FaDQ9H8HVBMpnnLFeejfZ8VVlvhc0uhm4EWQgnicGK7sigBte	999888777	admin	NDUWYFSJDFPHZL5ENUSL5OL46GJV54N3	\N	0.00
3	Employee 1	bankemp1	$2b$12$tw3c5Kc5DVjZrp3ZZx.O4.3NJ0z86R1oHAvT.Ii3RhAIU074YRYGy	112233	employee	CJDBCX7BPRZ2WNDRS35MF3YMIICAWEUD	f	0.00
6	Didi Riyadi	didi	$2b$12$7mLfzyCOtv3Pb4XjJIbdNOJqbOW8/mUDSdMVjPPRBP64DbUY.8ac.	87867423	customer	YSGQ6Q56DSUTUW6YKKKQI7ZNT7NDT363	t	4265.00
5	Edwin Son	edwin	$2b$12$zKjCkMjmveVnPzh4RNDBmuh2lWsOso9UN0CKtSWRSMEsOerEfPAV2	123456789	customer	ZADTYAZG75UIKRRPULPW5VTHUTG2UNRL	t	5735.00
8	Rudi Santoso	rudi	$2b$12$sVdkYpbz.bFDcfLOSMKQTOtOtDYbiAhQQJ2g1v3d296WK/cFaiMka	3242434	customer	UU5ODBGATFRARYKLYANKKGIMUJKR6L47	t	0.00
\.


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_mybank
--

SELECT pg_catalog.setval('public.transactions_id_seq', 7, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user_mybank
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- Name: users users_id_number_key; Type: CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_id_number_key UNIQUE (id_number);


--
-- Name: users users_otp_secret_key; Type: CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_otp_secret_key UNIQUE (otp_secret);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_transactions_id; Type: INDEX; Schema: public; Owner: user_mybank
--

CREATE INDEX ix_transactions_id ON public.transactions USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: user_mybank
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: transactions transactions_receiver_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_receiver_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: transactions transactions_sender_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user_mybank
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_sender_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

