--
-- PostgreSQL database dump
--

\restrict NtoZu2ufG7yllxf9E7pIc7TggG6jwAt1JBU1Fldu7vhXw80NNahsablkRKT07rU

-- Dumped from database version 16.10 (Debian 16.10-1.pgdg13+1)
-- Dumped by pg_dump version 16.10 (Homebrew)

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

--
-- Data for Name: blusas; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.blusas (id, talla, color, tipo, imagen, stock) FROM stdin;
1	S	Beige	Blusa	imagen61.jpeg	8
2	M	Azul	Blusa	imagen62.jpeg	10
3	L	Rosado	Blusa	imagen63.jpeg	12
5	M	Blanco	Blusa	imagen65.jpeg	16
4	S	Negro	Blusa	imagen64.jpeg	10
\.


--
-- Data for Name: blusones; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.blusones (id, talla, color, tipo, imagen, stock) FROM stdin;
1	XL	Rosado	Blusones	imagen17.jpeg	10
2	XL	Salmon	Blusones	imagen15.jpeg	8
3	XL	Blanco y Negro	Blusones	imagen18.jpeg	12
4	XL	Salmon	Blusones	imagen15.jpeg	5
5	XL	Gris	Blusones	imagen16.jpeg	8
\.


--
-- Data for Name: compras; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.compras (id, nombre_cliente, direccion, telefono, producto, cantidad, total, fecha) FROM stdin;
1	camilo	kakka	3232323809	Blusa - talla M, Color Blanco	4	80.00	2025-11-08 23:47:02.061589
2	martin	jahsjah	3232323809	Blusa - talla S, Color Negro	4	80.00	2025-11-08 23:47:15.171418
3	may	jaajja	3232323809	Blusa - talla S, Color Negro	4	80.00	2025-11-08 23:53:09.408895
4	camilo	kakka	3232323	Bluson - talla XL, Color Gris	1	25.00	2025-11-11 02:45:37.397222
\.


--
-- Data for Name: enterizos; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.enterizos (id, talla, color, tipo, imagen, stock) FROM stdin;
1	L	Azul	Enterizo	imagen31.jpeg	10
2	L	Azul	Enterizo	imagen32.jpeg	8
3	L	Azul	Enterizo	imagen33.jpeg	12
4	L	Azul	Enterizo	imagen34.jpeg	5
6	L	Azul	Enterizo	imagen31.jpeg	10
7	L	Azul	Enterizo	imagen32.jpeg	8
8	L	Azul	Enterizo	imagen33.jpeg	12
9	L	Azul	Enterizo	imagen34.jpeg	5
11	L	Azul	Enterizo	imagen31.jpeg	10
12	L	Azul	Enterizo	imagen32.jpeg	8
13	L	Azul	Enterizo	imagen33.jpeg	12
14	L	Azul	Enterizo	imagen34.jpeg	5
16	L	Azul	Enterizo	imagen31.jpeg	10
17	L	Azul	Enterizo	imagen32.jpeg	8
18	L	Azul	Enterizo	imagen33.jpeg	12
19	L	Azul	Enterizo	imagen34.jpeg	5
\.


--
-- Data for Name: jeans; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.jeans (id, talla, color, tipo, imagen, stock) FROM stdin;
1	L	Azul	Jean	imagen43.jpeg	8
2	L	Azul	Jean	imagen44.jpeg	10
3	L	Azul	Jean	imagen45.jpeg	12
4	L	Azul	Jean	imagen46.jpeg	14
5	L	Azul	Jean	imagen47.jpeg	16
6	L	Azul	Jean	imagen48.jpeg	18
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.transactions (id, tx_id, amount, currency, status, method, card_last4, card_brand, created_at) FROM stdin;
1	FP8F9XB5L7SC	20.00	USD	success	card_fake	1111	UNKNOWN	2025-11-09 05:00:24.275122
2	37TBXC8WNAZM	20.00	USD	success	card_fake	1111	UNKNOWN	2025-11-09 05:05:42.576161
3	TOQNLESKBMYI	60.00	USD	success	card_fake	1111	UNKNOWN	2025-11-09 05:06:11.214937
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.usuarios (id, nombre_usuario, contrasena_hash, nombre_completo, email, telefono, direccion, fecha_registro, rol) FROM stdin;
1	mariela	scrypt:32768:8:1$0NcVPulIF8oVH3Vs$7efe8e7372425bf1eebc12909572cd49535ebe45c8ac5f7f5c499fa3eb7ddb34b0627b66343600b847f5255556a5dacd24e9f8a9f6193f8e6651f59789232926	mariela	mariela@gmail.com	2134567890	aaaaaa	2025-11-09 03:24:25.509998	cliente
2	dulfa2	scrypt:32768:8:1$EZI8VYVNLwMxC0q3$ccfe3dc884b2b117fd1b111e4062d6e06b6276150cfae7590eb86f1742d872a9adc3b3bc7416359794af92b73ce53986d0e4c6f7bd78710d8445cc446bad66f4	dulfa	dulfa@gmail.com	3232323809	Carrera 17a # 9-54	2025-11-11 02:41:51.747759	cliente
\.


--
-- Data for Name: vestidos; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.vestidos (id, talla, color, tipo, imagen, stock) FROM stdin;
1	XL	Blanco y Negro	Vestido	imagen27.jpeg	8
2	XL	Blanco y Negro	Vestido	imagen23.jpeg	10
3	XL	Azul	Vestido	imagen24.jpeg	12
4	XL	Beige	Vestido	imagen25.jpeg	14
5	XL	Azul	Vestido	imagen24.jpeg	16
\.


--
-- Data for Name: vestidosgala; Type: TABLE DATA; Schema: public; Owner: tienda
--

COPY public.vestidosgala (id, talla, color, tipo, imagen, stock) FROM stdin;
1	XL	Rojo	Vestido de Gala	imagen53.jpeg	8
2	XL	Verde	Vestido de Gala	imagen54.jpeg	10
3	XL	Verde	Vestido de Gala	imagen51.jpeg	12
4	XL	Beige	Vestido de Gala	imagen52.jpeg	14
5	XL	Verde	Vestido de Gala	imagen54.jpeg	16
6	XL	Rojo	Vestido de Gala	imagen53.jpeg	18
\.


--
-- Name: blusas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.blusas_id_seq', 5, true);


--
-- Name: blusones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.blusones_id_seq', 55, true);


--
-- Name: compras_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.compras_id_seq', 4, true);


--
-- Name: enterizos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.enterizos_id_seq', 20, true);


--
-- Name: jeans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.jeans_id_seq', 6, true);


--
-- Name: transactions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.transactions_id_seq', 3, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 2, true);


--
-- Name: vestidos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.vestidos_id_seq', 5, true);


--
-- Name: vestidosgala_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tienda
--

SELECT pg_catalog.setval('public.vestidosgala_id_seq', 6, true);


--
-- PostgreSQL database dump complete
--

\unrestrict NtoZu2ufG7yllxf9E7pIc7TggG6jwAt1JBU1Fldu7vhXw80NNahsablkRKT07rU

