from elasticsearch import Elasticsearch

def setting():
    es=Elasticsearch()
    es.indices.create(
    index='brand-search',
    body={
        "mappings": {
            "properties": {
                "id": {
                    "type": "keyword"
                },

                "menu_id": {
                    "type": "integer"
                },
                "article_id": {
                    "type": "integer"
                },
                "user_id": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text",
                    "analyzer": "brand_analyzer"
                },
                "post_content": {
                    "type": "text",
                    "analyzer": "brand_analyzer"
                },


                "views": {
                    "type": "integer"
                },
                "post_reg_date": {
                    "type": "keyword"
                }

            }
        },
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "basic_analyzer": {
                            "filter": [
                                "nori_readingform",
                                "lowercase"
                            ],
                            "tokenizer": "nori_tokenizer"
                        },
                        "brand_analyzer": {
                            "filter": [
                                "nori_readingform",
                                "lowercase",
                                "synonym"
                            ],
                            "tokenizer": "brand_dict"
                        }
                    },
                    "tokenizer": {
                        "brand_dict": {
                            "decompound_mode": "NONE",
                            "type": "nori_tokenizer",
                            "user_dictionary": "brand.txt"
                        }

                    },
                    "char_filter": {
                        "phone_char_filter": {
                            "type": "pattern_replace",
                            "pattern": "[-./() ]",
                            "replacement": ""
                        }
                    },
                    "filter": {
                        "brand_keep": {
                            "type": "keep",
                            "keep_words_path": "brand.txt"
                        },
                        "npos_filter": {
                            "type": "nori_part_of_speech",
                            "stoptags": [
                                "E",
                                "IC",
                                "J",
                                "MAG",
                                "MM",
                                "SP",
                                "SSC",
                                "SSO",
                                "SC",
                                "SE",
                                "XPN",
                                "XSA",
                                "XSN",
                                "XSV",
                                "UNA",
                                "NA",
                                "VSV"
                            ]
                        },
                        "synonym": {
                            "type": "synonym",
                            "synonyms_path": "brandsynonym.txt"
                        }
                    }
                }
            }
        }
    }
    )