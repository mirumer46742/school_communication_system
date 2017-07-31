$(document).ready(function(){


    $('#contact_form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            first_name: {
                validators: {
                        stringLength: {
                        min: 2,
                    },
                        notEmpty: {
                        message: 'Please provide your first name'
                    }
                }
            },
            last_name: {
                validators: {
                    stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Please provide your last name'
                    }
                }
            },
            parentage: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Please provide your parentage'
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {
                        message: 'Please provide your email address'
                    },
                    emailAddress: {
                        message: 'Please provide a valid email address in proper format'
                    }
                }
            },
            phone: {
                validators: {
                    notEmpty: {
                        message: 'Please provide your phone number'
                    },
                    phone: {
                        country: 'IN',
                        message: 'Please provide a vaild phone number'
                    }
                }
            },
            address: {
                validators: {
                     stringLength: {
                        min: 4,
                    },
                    notEmpty: {
                        message: 'Please provide your street address'
                    }
                }
            },
            city: {
                validators: {
                     stringLength: {
                        min: 4,
                    },
                    notEmpty: {
                        message: 'Please provide your city'
                    }
                }
            },
            state: {
                validators: {
                    notEmpty: {
                        message: 'Please select your state'
                    }
                }
            },
            class: {
                validators: {
                    notEmpty: {
                        message: 'Please select the class'
                    }
                }
            },
            section: {
                validators: {
                    notEmpty: {
                        message: 'Please select the section'
                    }
                }
            },
            roll_no: {
                validators: {
                    notEmpty: {
                        message: 'Please provide roll no.'
                    },
                    numeric: {
                        message: 'The Roll No. must be a number'
                    },
                    stringLength: {
                        min: 1,
                        max: 3,
                    }
                }
            },
            zip: {
                validators: {
                    notEmpty: {
                        message: 'Please provide your zip code'
                    },
                    stringLength: {
                        min: 6,
                        max: 6,
                    }
                }
            },
            comment: {
                validators: {
                      stringLength: {
                        min: 10,
                        max: 200,
                        message:'Please enter at least 10 characters and no more than 200'
                    },
                    notEmpty: {
                        message: 'Please provide a description of your project'
                    }
                }
            }
        }
    });
  

    $('#edit_contact_form').bootstrapValidator({
        // To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            edit_first_name: {
                validators: {
                        stringLength: {
                        min: 2,
                    },
                        notEmpty: {
                        message: 'Please provide your first name'
                    }
                }
            },
            edit_last_name: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Please provide your last name'
                    }
                }
            },
            edit_parentage: {
                validators: {
                     stringLength: {
                        min: 2,
                    },
                    notEmpty: {
                        message: 'Please provide your parentage'
                    }
                }
            },
            edit_email: {
                validators: {
                    notEmpty: {
                        message: 'Please provide your email address'
                    },
                    emailAddress: {
                        message: 'Please provide a valid email address in proper format'
                    }
                }
            },
            edit_phone: {
                validators: {
                    notEmpty: {
                        message: 'Please provide your phone number'
                    },
                    phone: {
                        country: 'IN',
                        message: 'Please provide a vaild phone number'
                    }
                }
            },
            edit_address: {
                validators: {
                     stringLength: {
                        min: 4,
                    },
                    notEmpty: {
                        message: 'Please provide your street address'
                    }
                }
            },
            edit_city: {
                validators: {
                     stringLength: {
                        min: 4,
                    },
                    notEmpty: {
                        message: 'Please provide your city'
                    }
                }
            },
            edit_state: {
                validators: {
                    notEmpty: {
                        message: 'Please select your state'
                    }
                }
            },
            edit_class: {
                validators: {
                    notEmpty: {
                        message: 'Please select the class'
                    }
                }
            },
            edit_section: {
                validators: {
                    notEmpty: {
                        message: 'Please select the section'
                    }
                }
            },
            edit_roll_no: {
                validators: {
                    notEmpty: {
                        message: 'Please provide roll no.'
                    },
                    numeric: {
                        message: 'The roll no. must be a number'
                    },
                    stringLength: {
                        min: 1,
                        max: 3,
                    }
                }
            },
            edit_zip: {
                validators: {
                    notEmpty: {
                        message: 'Please provide your zip code'
                    },
                    stringLength: {
                        min: 6,
                        max: 6,
                    }
                }
            },
            edit_comment: {
                validators: {
                      stringLength: {
                        min: 10,
                        max: 200,
                        message:'Please enter at least 10 characters and no more than 200'
                    },
                    notEmpty: {
                        message: 'Please provide a description of your project'
                    }
                }
            }
        }
    });
});
    


    /*  $('#select_all').click(function() {
            if ($(this).is(':checked')) {
                $('td input').attr('checked', true);
            } else {
                $('td input').attr('checked', false);
            }
        });
    */


