"""
Konvensional decision tree for BTN product recommendations.

Node schema:
- Question node:
  {
    "text": "...",
    "choices": {
       "choice_key": {"label": "...", "next": "node_id"},
       ...
    },
    "meta": {... optional ...}
  }

- Leaf node:
  {
    "leaf": True,
    "products": [...],
    "links": [...],  # optional, fill with BTN product page links later
    "meta": {... optional ...}
  }
"""

TREE = {
    # -------------------------
    # ROOT
    # -------------------------
    "q1": {
        "text": "Are you using BTN as:",
        "choices": {
            "individual": {"label": "Individual / Personal", "next": "ind_q2_goal"},
            "business": {"label": "Business / Institution", "next": "biz_q2_goal"},
        },
        "meta": {"segment": "konven"},
    },

    # =====================================================================
    # A. INDIVIDUAL / PERSONAL
    # =====================================================================
    "ind_q2_goal": {
        "text": "What is your main goal?",
        "choices": {
            "saving": {"label": "Daily banking / saving", "next": "ind_saving_q3"},
            "property": {"label": "Property (housing)", "next": "ind_property_q3"},
            "loan": {"label": "Borrowing money (non-property)", "next": "ind_loan_q3"},
            "services": {"label": "Payments & services", "next": "ind_services_q3"},
            "invest": {"label": "Investing", "next": "ind_invest_q3"},
        },
        "meta": {"customer_type": "individual"},
    },

    # -------------------------
    # A1. Daily banking / saving
    # -------------------------
    "ind_saving_q3": {
        "text": "What kind of saving/banking do you need?",
        "choices": {
            "everyday": {"label": "Simple everyday banking", "next": "ind_saving_everyday_q4"},
            "goal": {"label": "Saving for a goal", "next": "ind_saving_goal_q4"},
            "fx": {"label": "Foreign currency savings", "next": "leaf_tabungan_btn_felas"},
            "student": {"label": "Student / child", "next": "ind_saving_student_q4"},
            "community": {"label": "Community / special institution", "next": "leaf_community_special"},
            "business": {"label": "Business transactions (high limits, EDC/QRIS, or cheque/giro)", "next": "ind_saving_business_q4"},
        },
        "meta": {"goal": "saving"},
    },

    "ind_saving_goal_q4": {
        "text": "What is your saving goal type?",
        "choices": {
            "short_medium": {"label": "Short–medium term", "next": "leaf_tabungan_btn_siap"},
            "long_housing": {"label": "Long-term housing", "next": "leaf_tabungan_btn_simuda_rumahku"},
            "parking_cash": {"label": "Parking excess cash", "next": "leaf_tabungan_btn_investa"},
        },
        "meta": {"goal": "saving"},
    },

    "ind_saving_student_q4": {
        "text": "Student / child age group?",
        "choices": {
            "3_17": {"label": "Age 3–17", "next": "leaf_tabungan_btn_simpel"},
            "0_23": {"label": "Age 0–23", "next": "leaf_tabungan_btn_juara"},
        },
        "meta": {"goal": "saving"},
    },

    "ind_saving_everyday_q4": {
        "text": "Which type of everyday savings account fits you best?",
        "choices": {
            "standard": {"label": "Standard everyday banking", "next": "leaf_tabungan_btn_batara"},
            "basic": {"label": "Basic account with light requirements", "next": "leaf_tabunganku"},
        },
        "meta": {"goal": "saving"},
    },

    "ind_saving_business_q4": {
        "text": "Which business account type do you need?",
        "choices": {
            "high_limit_payments": {"label": "High transaction limits + EDC/QRIS (business operations)", "next": "leaf_tabungan_btn_bisnis_individual"},
            "giro_cheque": {"label": "Cheque/giro-style flexibility & frequent withdrawals (current account)", "next": "leaf_giro_perorangan"},
        },
        "meta": {"goal": "saving"},
    },

    # Leaves for A1
    "leaf_tabungan_btn_batara": {
        "leaf": True,
        "products": ["Tabungan BTN Batara"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-Batara"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabungan_btn_siap": {
        "leaf": True,
        "products": ["Tabungan BTN Siap"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Investasi-Berjangka/Tabungan-BTN-Siap"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabungan_btn_simuda_rumahku": {
        "leaf": True,
        "products": ["Tabungan BTN SiMuda RumahKu"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Investasi-Berjangka/Tabungan-BTN-SiMuda-RumahKu"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabungan_btn_investa": {
        "leaf": True,
        "products": ["Tabungan BTN Investa"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Investasi-Berjangka/Tabungan-BTN-Investa"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabungan_btn_felas": {
        "leaf": True,
        "products": ["Tabungan BTN Felas"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-Felas"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabungan_btn_simpel": {
        "leaf": True,
        "products": ["Tabungan BTN SimPel"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Anak/Tabungan-BTN-SimPel"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabungan_btn_juara": {
        "leaf": True,
        "products": ["Tabungan BTN Juara"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Anak/Tabungan-BTN-Juara"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabunganku": {
        "leaf": True,
        "products": ["TabunganKu"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Transaksional/Tabunganku"],
        "meta": {"goal": "saving"},
    },
    "leaf_community_special": {
        "leaf": True,
        "products": ["Tabungan BTN HKBP", "Tabungan BTN e’BATARAPOS"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-HKBP", "https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-EBATARAPOS"],
        "meta": {"goal": "saving"},
    },
    "leaf_tabungan_btn_bisnis_individual": {
        "leaf": True,
        "products": ["Tabungan BTN Bisnis"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-Bisnis"],
        "meta": {"goal": "saving"},
    },
    "leaf_giro_perorangan": {
        "leaf": True,
        "products": ["Giro Perorangan"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Giro/Giro-BTN-Perorangan"],
        "meta": {"goal": "saving"},
    },
    "leaf_kartu_debit_btn": {
        "leaf": True,
        "products": ["Kartu ATM/Debit BTN"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Kartu-Debit-BTN/Kartu-ATM-Debit-BTN"],
        "meta": {"goal": "services"},
    },
    "leaf_kartu_debit_btn_suka_suka": {
        "leaf": True,
        "products": ["Kartu ATM/Debit BTN Suka-Suka"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Kartu-Debit-BTN/Kartu-ATM-Debit-BTN-Suka---Suka"],
        "meta": {"goal": "services"},
    },
    "leaf_kartu_debit_btn_contactless_paywave": {
        "leaf": True,
        "products": ["Kartu ATM/Debit BTN Visa Contactless Paywave"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Kartu-Debit-BTN/Kartu-ATM-Debit-BTN-Visa-Contactless-Paywave"],
        "meta": {"goal": "services"},
    },

    # -------------------------
    # A2. Property (housing)
    # -------------------------
    "ind_property_q3": {
        "text": "What property need do you have?",
        "choices": {
            "first_home": {"label": "Buying first home", "next": "ind_property_first_home_q4"},
            "non_subsidized": {"label": "Buying non-subsidized house", "next": "leaf_kpr_btn_platinum"},
            "apartment": {"label": "Buying apartment", "next": "leaf_kpa_btn_platinum"},
            "ex_asset_btn": {"label": "Buying ex-BTN mortgage / ex-asset BTN (ready stock)", "next": "leaf_kpr_btn_maju"},
            "build_own_land": {"label": "Building on own land", "next": "ind_property_build_own_land_q4"},
            "renovation": {"label": "Renovating house", "next": "ind_property_renovation_q4"},
            "bale_member": {"label": "Already living in housing complex (balé community member)", "next": "leaf_bale_community_member"},
            "search_preapproval": {"label": "Searching property / pre-approval", "next": "leaf_btn_properti"},
        },
        "meta": {"goal": "property"},
    },

    "ind_property_first_home_q4": {
        "text": "Buying first home: which category best describes you?",
        "choices": {
            "mbr": {"label": "Low-income (MBR)", "next": "leaf_kpr_btn_sejahtera_flpp"},
            "asn": {"label": "ASN (civil servant)", "next": "leaf_kpr_btn_tapera"},
            "general": {"label": "General", "next": "leaf_kpr_btn_platinum"},
        },
        "meta": {"goal": "property"},
    },

    "ind_property_build_own_land_q4": {
        "text": "Building on own land: which category best describes you?",
        "choices": {
            "asn": {"label": "ASN", "next": "leaf_kbr_btn_tapera"},
            "general": {"label": "General", "next": "leaf_kredit_bangun_rumah"},
        },
        "meta": {"goal": "property"},
    },

    "ind_property_renovation_q4": {
        "text": "Renovating house: are you a participant of?",
        "choices": {
            "tapera": {"label": "Tapera", "next": "leaf_krr_btn_tapera"},
            "bpjs": {"label": "BPJS Ketenagakerjaan", "next": "leaf_prp_bpjs"},
        },
        "meta": {"goal": "property"},
    },

    # Leaves for A2
    "leaf_kpr_btn_sejahtera_flpp": {
        "leaf": True,
        "products": ["KPR BTN Sejahtera (FLPP)"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KPR-BTN-Sejahtera-FLPP"],
        "meta": {"goal": "property"},
    },
    "leaf_kpr_btn_tapera": {
        "leaf": True,
        "products": ["KPR BTN Tapera"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KPR-BTN-Tapera"],
        "meta": {"goal": "property"},
    },
    "leaf_kpr_btn_platinum": {
        "leaf": True,
        "products": ["KPR BTN Platinum"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KPR-BTN-Platinum"],
        "meta": {"goal": "property"},
    },
    "leaf_kpa_btn_platinum": {
        "leaf": True,
        "products": ["KPA BTN Platinum"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KPA-BTN-Platinum"],
        "meta": {"goal": "property"},
    },
    "leaf_kbr_btn_tapera": {
        "leaf": True,
        "products": ["KBR BTN Tapera"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KBR-BTN-Tapera"],
        "meta": {"goal": "property"},
    },
    "leaf_kredit_bangun_rumah": {
        "leaf": True,
        "products": ["Kredit Bangun Rumah"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/Kredit-Bangun-Rumah-BTN"],
        "meta": {"goal": "property"},
    },
    "leaf_krr_btn_tapera": {
        "leaf": True,
        "products": ["KRR BTN Tapera"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KRR-BTN-Tapera"],
        "meta": {"goal": "property"},
    },
    "leaf_prp_bpjs": {
        "leaf": True,
        "products": ["PRP BPJS"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/Fasilitas-Pembiayaan-Perumahan-Kerjasama-dengan-BPJS-Ketenagakerjaan"],
        "meta": {"goal": "property"},
    },
    "leaf_bale_community_member": {
        "leaf": True,
        "products": ["balé community (Anggota)"],
        "links": ["https://www.btn.co.id/id/Individual/Digital-Mortgage/Digital-Mortgage-Platform/bale-community-Anggota-Komunitas"],
        "meta": {"goal": "property"},
    },
    "leaf_btn_properti": {
        "leaf": True,
        "products": ["BTN Properti"],
        "links": ["https://www.btn.co.id/id/Individual/Digital-Mortgage/Digital-Mortgage-Platform/BTN-Properti"],
        "meta": {"goal": "property"},
    },
    "leaf_kpr_btn_maju": {
        "leaf": True,
        "products": ["KPR BTN Maju"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KPR-BTN-Maju"],
        "meta": {"goal": "property"},
    },

    # -------------------------
    # A3. Borrowing money (non-property)
    # -------------------------
    "ind_loan_q3": {
        "text": "What kind of borrowing do you need?",
        "choices": {
            "with_collateral": {"label": "Using property as collateral", "next": "leaf_kredit_agunan_rumah_btn"},
            "without_collateral": {"label": "Without collateral", "next": "ind_loan_without_collateral_q4"},
            "credit_card": {"label": "Credit card", "next": "leaf_kartu_kredit_btn"},
        },
        "meta": {"goal": "loan"},
    },

    "ind_loan_without_collateral_q4": {
        "text": "Without collateral: which category best describes you?",
        "choices": {
            "employee": {"label": "Active employee", "next": "leaf_kring_btn"},
            "pensioner": {"label": "Pensioner", "next": "leaf_kredit_ringan_btn_pensiunan"},
            "molis": {"label": "Electric motorcycle (Product)", "next": "leaf_kring_btn_molis"},
        },
        "meta": {"goal": "loan"},
    },

    # Leaves for A3
    "leaf_kredit_agunan_rumah_btn": {
        "leaf": True,
        "products": ["Kredit Agunan Rumah BTN"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/Kredit-Agunan-Rumah-BTN"],
        "meta": {"goal": "loan"},
    },
    "leaf_kring_btn": {
        "leaf": True,
        "products": ["KRING BTN"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KRING-BTN"],
        "meta": {"goal": "loan"},
    },
    "leaf_kredit_ringan_btn_pensiunan": {
        "leaf": True,
        "products": ["Kredit Ringan BTN Pensiunan"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KRING-BTN-Pensiunan"],
        "meta": {"goal": "loan"},
    },
    "leaf_kring_btn_molis": {
        "leaf": True,
        "products": ["KRING BTN Molis"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Produk-Kredit/KRING-BTN-Molis"],
        "meta": {"goal": "loan"},
    },
    "leaf_kartu_kredit_btn": {
        "leaf": True,
        "products": ["Kartu Kredit BTN"],
        "links": ["https://www.btn.co.id/id/Individual/Kredit-Konsumer/Kartu-Kredit-BTN/Kartu-Kredit-BTN"],
        "meta": {"goal": "loan"},
    },

    # -------------------------
    # A4. Payments & services
    # -------------------------
    "ind_services_q3": {
        "text": "What services do you need?",
        "choices": {
            "digital": {"label": "Digital banking", "next": "leaf_bale_by_btn"},
            "cashless": {"label": "Cashless daily payments", "next": "leaf_kartu_prepaid_btn_blink"},
            "intl": {"label": "International transfers", "next": "leaf_intl_transfer"},
            "bills": {"label": "Bills & public services", "next": "ind_bills_q4"},
            "sdb": {"label": "Secure storage", "next": "leaf_safe_deposit_box"},
            "debit_card": {"label": "ATM/Debit card", "next": "ind_services_debit_card_q4"},
            "internet_banking": {"label": "Internet Banking", "next": "leaf_btn_internet_banking"},
            "agent_btn": {"label": "Become an Agent (Laku Pandai - Agen BTN)", "next": "leaf_agen_btn_laku_pandai"},
        },
        "meta": {"goal": "services"},
    },

    "ind_bills_q4": {
        "text": "What kind of bills do you need to pay?",
        "choices": {
            "pdam": {"label": "PDAM", "next": "leaf_pdam"},
            "pajak_kendaraan": {"label": "Pajak Kendaraan", "next": "leaf_pajak_kendaraan"},
            "education": {"label": "Education", "next": "ind_education_q5"},
        },
        "meta": {"goal": "services"},
    },

    "ind_education_q5": {
        "text": "What kind of education payments?",
        "choices": {
            "spp": {"label": "SPP", "next": "leaf_spp"},
            "ptn": {"label": "UTBK and SMM PTN-Barat", "next": "leaf_ptn"},
        },
        "meta": {"goal": "services"},
    },

    "ind_services_debit_card_q4": {
        "text": "Which debit card option are you looking for?",
        "choices": {
            "standard": {"label": "Standard BTN Debit Card options (Reguler / Prioritas)", "next": "leaf_kartu_debit_btn"},
            "custom_design": {"label": "Custom design card (Suka-Suka)", "next": "leaf_kartu_debit_btn_suka_suka"},
            "contactless": {"label": "Contactless (Visa Contactless Paywave)", "next": "leaf_kartu_debit_btn_contactless_paywave"},
        },
        "meta": {"goal": "services"},
    },

    # Leaves for A4
    "leaf_bale_by_btn": {
        "leaf": True,
        "products": ["balé by BTN"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/e-Channels/bale-by-BTN"],
        "meta": {"goal": "services"},
    },
    "leaf_kartu_prepaid_btn_blink": {
        "leaf": True,
        "products": ["Kartu Prepaid BTN Blink"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/e-Channels/Kartu-Prepaid-BTN-Blink"],
        "meta": {"goal": "services"},
    },
    "leaf_intl_transfer": {
        "leaf": True,
        "products": ["SWIFT Transfer", "Finpay Remittance"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Tambahan/Pengiriman-uang-melalui-SWIFT", "https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Tambahan/Finpay-Remittance"],
        "meta": {"goal": "services"},
    },
    "leaf_pdam": {
        "leaf": True,
        "products": ["PDAM payments"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Transaksi/Pembayaran-PDAM"],
        "meta": {"goal": "services"},
    },
    "leaf_pajak_kendaraan": {
        "leaf": True,
        "products": ["Pajak Kendaraan payments"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Transaksi/Pembayaran-Pajak-Kendaraan-Jawa-Tengah"],
        "meta": {"goal": "services"},
    },
    "leaf_spp": {
        "leaf": True,
        "products": ["SPP payments"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Transaksi/SPP-Online"],
        "meta": {"goal": "services"},
    },
    "leaf_ptn": {
        "leaf": True,
        "products": ["SMM PTN-Barat payments"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Transaksi/Pembayaran-UTBK-dan-SMM-PTN-Barat"],
        "meta": {"goal": "services"},
    },
    "leaf_safe_deposit_box": {
        "leaf": True,
        "products": ["Safe Deposit Box"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Tambahan/Safe-Deposit-Box"],
        "meta": {"goal": "services"},
    },
    "leaf_agen_btn_laku_pandai": {
        "leaf": True,
        "products": ["Laku Pandai - Agen BTN"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/e-Channels/Agen-BTN"],
        "meta": {"goal": "services"},
    },
    "leaf_btn_internet_banking": {
        "leaf": True,
        "products": ["BTN Internet Banking"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/e-Channels/BTN-Internet-Banking"],
        "meta": {"goal": "services"},
    },

    # -------------------------
    # A5. Investing
    # -------------------------
    "ind_invest_q3": {
        "text": "What investment profile do you want?",
        "choices": {
            "fixed_deposit": {"label": "Low-risk fixed deposit", "next": "ind_deposito_q4"},
            "higher_return": {"label": "Higher return investment", "next": "ind_invest_higher_return_q4"},
        },
        "meta": {"goal": "invest"},
    },

    "ind_invest_higher_return_q4": {
        "text": "Higher return investment type?",
        "choices": {
            "principal_protected": {"label": "Principal protected", "next": "leaf_swap_depo"},
            "market_linked": {"label": "Market-linked", "next": "leaf_mld"},
            "fx_based": {"label": "FX-based", "next": "leaf_dci"},
        },
        "meta": {"goal": "invest"},
    },

    "ind_deposito_q4": {
        "text": "Currency Type?",
        "choices": {
            "rupiah": {"label": "Rupiah", "next": "leaf_deposito_btn"},
            "valas": {"label": "Valas", "next": "leaf_deposito_btn_valas"},
        },
        "meta": {"goal": "invest"},
    },

    # Leaves for A5
    "leaf_deposito_btn": {
        "leaf": True,
        "products": ["Deposito BTN Rupiah"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Produk-Investasi/Deposito-BTN-Ritel-Rupiah"],
        "meta": {"goal": "invest"},
    },
    "leaf_deposito_btn_valas": {
        "leaf": True,
        "products": ["Deposito BTN Valas"],
        "links": ["https://www.btn.co.id/id/Individual/Produk-Dana/Produk-Investasi/Deposito-BTN-Ritel-Valas"],
        "meta": {"goal": "invest"},
    },
    "leaf_swap_depo": {
        "leaf": True,
        "products": ["Swap Depo"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Tambahan/Swap-Depo"],
        "meta": {"goal": "invest"},
    },
    "leaf_mld": {
        "leaf": True,
        "products": ["Market Linked Deposit (MLD)"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Tambahan/Market-Linked-Deposit"],
        "meta": {"goal": "invest"},
    },
    "leaf_dci": {
        "leaf": True,
        "products": ["Dual Currency Investment (DCI)"],
        "links": ["https://www.btn.co.id/id/Individual/Jasa-Layanan/Layanan-Tambahan/Dual-Currency-Investment"],
        "meta": {"goal": "invest"},
    },

    # =====================================================================
    # B. BUSINESS / INSTITUTION
    # =====================================================================
    "biz_q2_goal": {
        "text": "What is your main goal?",
        "choices": {
            "ops": {"label": "Daily operations & banking", "next": "biz_ops_q3"},
            "financing": {"label": "Financing / loans", "next": "biz_financing_q3"},
            "property_dev": {"label": "Property development", "next": "biz_property_dev_q3"},
            "automation": {"label": "Payments, payroll & automation", "next": "biz_automation_q3"},
            "trade": {"label": "Trade finance & guarantees", "next": "biz_trade_q3"},
        },
        "meta": {"customer_type": "business"},
    },

    # -------------------------
    # B1. Daily operations & banking
    # -------------------------
    "biz_ops_q3": {
        "text": "What daily operations/banking do you need?",
        "choices": {
            "general": {"label": "General transactions", "next": "leaf_biz_tabungan_batara"},
            "high_volume": {"label": "High-volume transactions", "next": "leaf_tabungan_btn_bisnis"},
            "fx": {"label": "Foreign currency", "next": "leaf_biz_felas"},
            "cheque_bg": {"label": "Cheque / BG required", "next": "leaf_giro_lembaga"},
            "idle_funds": {"label": "Short-term idle funds", "next": "leaf_doc"},
            "special": {"label": "Special / community programs (HKBP, eBATARAPOS)", "next": "leaf_biz_tabungan_special"},
            "invest_savings": {"label": "Higher-yield savings (Investa)", "next": "leaf_biz_tabungan_investa"},
        },
        "meta": {"goal": "ops"},
    },

    # Leaves for B1
    "leaf_biz_tabungan_batara": {
        "leaf": True,
        "products": ["Tabungan BTN Batara (Business)"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-Batara"],
        "meta": {"goal": "ops"},
    },
    "leaf_tabungan_btn_bisnis": {
        "leaf": True,
        "products": ["Tabungan BTN Bisnis"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-Bisnis"],
        "meta": {"goal": "ops"},
    },
    "leaf_biz_felas": {
        "leaf": True,
        "products": ["Tabungan BTN Felas (Business)"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-Felas"],
        "meta": {"goal": "ops"},
    },
    "leaf_giro_lembaga": {
        "leaf": True,
        "products": ["Giro Lembaga"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Dana/Giro/Giro-Lembaga"],
        "meta": {"goal": "ops"},
    },
    "leaf_doc": {
        "leaf": True,
        "products": ["Deposito On Call (DOC)"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Dana/Deposito/Deposito-On-Call"],
        "meta": {"goal": "ops"},
    },
    "leaf_biz_tabungan_special": {
        "leaf": True,
        "products": ["Tabungan BTN HKBP (Business)", "Tabungan BTN eBATARAPOS (Business)"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-HKBP", "https://www.btn.co.id/id/Business/Produk-Dana/Tabungan-Transaksional/Tabungan-BTN-eBATARAPOS"],
        "meta": {"goal": "ops"},
    },
    "leaf_biz_tabungan_investa": {
        "leaf": True,
        "products": ["Tabungan BTN Investa (Business)"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Dana/Tabungan-Investasi/Tabungan-BTN-Investa"],
        "meta": {"goal": "ops"},
    },

    # -------------------------
    # B2. Financing / loans
    # -------------------------
    "biz_financing_q3": {
        "text": "What type of financing do you need?",
        "choices": {
            "working_capital": {"label": "Working capital", "next": "biz_working_capital_q4"},
            "investment": {"label": "Investment / expansion", "next": "leaf_kredit_investasi"},
            "umkm": {"label": "UMKM", "next": "biz_umkm_q4"},
        },
        "meta": {"goal": "financing"},
    },

    "biz_working_capital_q4": {
        "text": "Working capital type?",
        "choices": {
            "general": {"label": "General", "next": "leaf_kredit_modal_kerja"},
            "contractor": {"label": "Contractor", "next": "leaf_kmk_kontraktor"},
            "property_project": {"label": "Property project", "next": "leaf_kmk_properti"},
            "deposit_backed": {"label": "Deposit-backed", "next": "leaf_kredit_beragunan_simpanan"},
            "supply_chain": {"label": "Supply chain financing (seller/buyer)", "next": "leaf_supply_chain_financing"},
        },
        "meta": {"goal": "financing"},
    },

    "biz_umkm_q4": {
        "text": "UMKM category?",
        "choices": {
            "kur": {"label": "Micro / small (KUR)", "next": "leaf_kur"},
            "btn_laku": {"label": "Easy UMKM loan solution (BTN LAKU)", "next": "leaf_btn_laku"},
            "umkm_mk": {"label": "Growing UMKM (Working Capital)", "next": "leaf_kredit_umkm_modal_kerja"},
            "umkm_inv": {"label": "Long-term (Investment)", "next": "leaf_kredit_umkm_investasi"},
            "linkage": {"label": "Via BPR / Koperasi", "next": "leaf_umkm_linkage_program"},
        },
        "meta": {"goal": "financing"},
    },

    # Leaves for B2
    "leaf_kredit_modal_kerja": {
        "leaf": True,
        "products": ["Kredit Modal Kerja"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha/Kredit-Modal-Kerja"],
        "meta": {"goal": "financing"},
    },
    "leaf_kmk_kontraktor": {
        "leaf": True,
        "products": ["Kredit Modal Kerja Kontraktor"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha/Kredit-Modal-Kerja-Kontraktor"],
        "meta": {"goal": "financing"},
    },
    "leaf_kmk_properti": {
        "leaf": True,
        "products": ["Kredit Modal Kerja Properti"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha/Kredit-Modal-Kerja-Properti-BTN"],
        "meta": {"goal": "financing"},
    },
    "leaf_kredit_beragunan_simpanan": {
        "leaf": True,
        "products": ["Kredit Beragunan Simpanan"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha/Kredit-Modal-Kerja-Beragunan-Simpanan"],
        "meta": {"goal": "financing"},
    },
    "leaf_kredit_investasi": {
        "leaf": True,
        "products": ["Kredit Investasi"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha/Kredit-Investasi"],
        "meta": {"goal": "financing"},
    },
    "leaf_kur": {
        "leaf": True,
        "products": ["Kredit Usaha Rakyat (KUR)"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha-Mikro-Kecil-Menengah/KUR-Kredit-Usaha-Rakyat"],
        "meta": {"goal": "financing"},
    },
    "leaf_supply_chain_financing": {
        "leaf": True,
        "products": ["Supply Chain Financing"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Supply-Chain-Financing"],
        "meta": {"goal": "financing"},
    },
    "leaf_kredit_umkm_modal_kerja": {
        "leaf": True,
        "products": ["Kredit UMKM Modal Kerja"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha-Mikro-Kecil-Menengah/Kredit-UMKM-Modal-Kerja"],
        "meta": {"goal": "financing"},
    },
    "leaf_kredit_umkm_investasi": {
        "leaf": True,
        "products": ["Kredit UMKM Investasi"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha-Mikro-Kecil-Menengah/Kredit-UMKM-Investasi"],
        "meta": {"goal": "financing"},
    },
    "leaf_umkm_linkage_program": {
        "leaf": True,
        "products": ["UMKM Linkage Program"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha-Mikro-Kecil-Menengah/Kredit-UMKM-Linkage-Program"],
        "meta": {"goal": "financing"},
    },
    "leaf_btn_laku": {
        "leaf": True,
        "products": ["BTN LAKU"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha-Mikro-Kecil-Menengah/BTN-LAKU"],
        "meta": {"goal": "financing"},
    },

    # -------------------------
    # B3. Property development
    # -------------------------
    "biz_property_dev_q3": {
        "text": "Property development need?",
        "choices": {
            "build_project": {"label": "Building housing project", "next": "leaf_kredit_konstruksi_btn"},
            "buy_land": {"label": "Buying land", "next": "leaf_kredit_kepemilikan_lahan"},
            "gov_program": {"label": "Government housing program", "next": "biz_gov_program_q4"},
            "sell_digitally": {"label": "Selling units digitally", "next": "leaf_btn_properti_for_developer"},
            "manage_residence": {"label": "Managing residence", "next": "leaf_bale_community_pengelola"},
        },
        "meta": {"goal": "property_dev"},
    },

    "biz_gov_program_q4": {
        "text": "Government housing program: supply or demand side?",
        "choices": {
            "supply": {"label": "Supply side", "next": "leaf_kpp_btn_penyediaan"},
            "demand": {"label": "Demand side", "next": "leaf_kpp_btn_permintaan"},
        },
        "meta": {"goal": "property_dev"},
    },

    # Leaves for B3
    "leaf_kredit_konstruksi_btn": {
        "leaf": True,
        "products": ["Kredit Konstruksi BTN"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha/Kredit-Konstruksi-Bank-BTN"],
        "meta": {"goal": "property_dev"},
    },
    "leaf_kredit_kepemilikan_lahan": {
        "leaf": True,
        "products": ["Kredit Kepemilikan Lahan"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha/Kredit-Kepemilikan-Lahan"],
        "meta": {"goal": "property_dev"},
    },
    "leaf_kpp_btn_penyediaan": {
        "leaf": True,
        "products": ["KPP BTN Penyediaan"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha-Mikro-Kecil-Menengah/Kredit-Program-Perumahan-BTN-Sisi-Penyediaan-Rumah"],
        "meta": {"goal": "property_dev"},
    },
    "leaf_kpp_btn_permintaan": {
        "leaf": True,
        "products": ["KPP BTN Permintaan"],
        "links": ["https://www.btn.co.id/id/Business/Produk-Komersial/Kredit-Usaha-Mikro-Kecil-Menengah/Kredit-Program-Perumahan-BTN-Sisi-Permintaan"],
        "meta": {"goal": "property_dev"},
    },
    "leaf_btn_properti_for_developer": {
        "leaf": True,
        "products": ["BTN Properti for Developer"],
        "links": ["https://www.btn.co.id/id/Business/Digital-Mortgage/Digital-Mortgage-Platform/BTN-Properti-for-Developer"],
        "meta": {"goal": "property_dev"},
    },
    "leaf_bale_community_pengelola": {
        "leaf": True,
        "products": ["balé community (Pengelola)"],
        "links": ["https://www.btn.co.id/id/Business/Digital-Mortgage/Digital-Mortgage-Platform/bale-community-Pengelola"],
        "meta": {"goal": "property_dev"},
    },

    # -------------------------
    # B4. Payments, payroll & automation
    # -------------------------
    "biz_automation_q3": {
        "text": "What payments/payroll/automation do you need?",
        "choices": {
            "payroll": {"label": "Payroll", "next": "leaf_payroll"},
            "cash_mgmt": {"label": "Cash management", "next": "biz_cash_mgmt_q4"},
            "merchant": {"label": "Merchant payments", "next": "biz_merchant_q4"},
            "billing": {"label": "Automated billing", "next": "leaf_virtual_account_btn"},
            "integration": {"label": "System integration", "next": "leaf_btn_open_api"},
            "securities": {"label": "Securities / capital market services", "next": "biz_securities_services_q4"},
            "token": {"label": "Security token for business banking (BTN Token)", "next": "leaf_btn_token"},
        },
        "meta": {"goal": "automation"},
    },

    "biz_cash_mgmt_q4": {
        "text": "Cash management for:",
        "choices": {
            "sme": {"label": "SME", "next": "leaf_bale_bisnis"},
            "corporate": {"label": "Corporate", "next": "leaf_bale_korpora"},
        },
        "meta": {"goal": "automation"},
    },

    "biz_merchant_q4": {
        "text": "Merchant payments type?",
        "choices": {
            "qris": {"label": "QR payments", "next": "leaf_qris_btn"},
            "edc": {"label": "Card payments", "next": "leaf_edc_btn"},
        },
        "meta": {"goal": "automation"},
    },

    "biz_securities_services_q4": {
        "text": "Which securities service do you need?",
        "choices": {
            "custodian": {"label": "Custodian services", "next": "leaf_jasa_kustodian"},
            "trustee": {"label": "Trustee (Wali Amanat)", "next": "leaf_wali_amanat"},
        },
        "meta": {"goal": "automation"},
    },

    # Leaves for B4
    "leaf_payroll": {
        "leaf": True,
        "products": ["BTN Payroll", "balé Solusi"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Jasa-Layanan-BTN-Payroll", "https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/bale-Solusi-by-BTN"],
        "meta": {"goal": "automation"},
    },
    "leaf_bale_bisnis": {
        "leaf": True,
        "products": ["balé bisnis"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/e-Channels/Bale-Bisnis"],
        "meta": {"goal": "automation"},
    },
    "leaf_bale_korpora": {
        "leaf": True,
        "products": ["balé korpora"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/e-Channels/bale-korpora-by-BTN"],
        "meta": {"goal": "automation"},
    },
    "leaf_qris_btn": {
        "leaf": True,
        "products": ["QRIS BTN"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/QRIS-BTN-Merchant"],
        "meta": {"goal": "automation"},
    },
    "leaf_edc_btn": {
        "leaf": True,
        "products": ["EDC BTN"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/e-Channels/EDC"],
        "meta": {"goal": "automation"},
    },
    "leaf_virtual_account_btn": {
        "leaf": True,
        "products": ["Virtual Account BTN"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Virtual-Account-BTN"],
        "meta": {"goal": "automation"},
    },
    "leaf_btn_open_api": {
        "leaf": True,
        "products": ["BTN Open API"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/e-Channels/BTN-Open-API"],
        "meta": {"goal": "automation"},
    },
    "leaf_jasa_kustodian": {
        "leaf": True,
        "products": ["Jasa Kustodian"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Jasa-Kustodian"],
        "meta": {"goal": "automation"},
    },
    "leaf_wali_amanat": {
        "leaf": True,
        "products": ["Wali Amanat"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Wali-Amanat"],
        "meta": {"goal": "automation"},
    },
    "leaf_btn_token": {
        "leaf": True,
        "products": ["BTN Token"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/BTN-Token"],
        "meta": {"goal": "automation"},
    },

    # -------------------------
    # B5. Trade finance & guarantees
    # -------------------------
    "biz_trade_q3": {
        "text": "Trade finance / guarantees need?",
        "choices": {
            "domestic_trade": {"label": "Domestic trade", "next": "leaf_skbdn"},
            "import_financing": {"label": "Import financing", "next": "leaf_trust_receipt"},
            "early_payment": {"label": "Early payment of documents", "next": "leaf_negotiation_discounting"},
            "collection": {"label": "Trade document collection", "next": "leaf_documentary_collection"},
            "guarantee": {"label": "Contract guarantees", "next": "leaf_bank_garansi_standby_lc"},
        },
        "meta": {"goal": "trade"},
    },

    # Leaves for B5
    "leaf_skbdn": {
        "leaf": True,
        "products": ["SKBDN"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Surat-Kredit-Berdokumen-Dalam-Negeri-Letter-of-Credit"],
        "meta": {"goal": "trade"},
    },
    "leaf_trust_receipt": {
        "leaf": True,
        "products": ["Trust Receipt"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Trust-Receipt"],
        "meta": {"goal": "trade"},
    },
    "leaf_negotiation_discounting": {
        "leaf": True,
        "products": ["Negotiation / Discounting"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Negosiasi-Diskonto-Surat-Kredit-Berdokumen-Dalam-Negeri-Letter-of-Credit"],
        "meta": {"goal": "trade"},
    },
    "leaf_documentary_collection": {
        "leaf": True,
        "products": ["Documentary Collection"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Documentary-Collection"],
        "meta": {"goal": "trade"},
    },
    "leaf_bank_garansi_standby_lc": {
        "leaf": True,
        "products": ["Bank Garansi / Standby LC"],
        "links": ["https://www.btn.co.id/id/Business/Jasa-Layanan/Layanan-Transaksi/Bank-Garansi"],
        "meta": {"goal": "trade"},
    },
}
