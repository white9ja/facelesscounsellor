ola.vicayo2016@gmail.com



ul>
                          {% endfor%}
                            {% for service in services %}  
                        <div class="tab-content">
                 
                            <div class="tab-pane fade active in" id="tab{{service.name}}">
                            <div style="padding: 5px 20px; ">
                            <center>
                                <p>{{service.meeting}} Section/Meeting In a Week</p>
                                <hr>
                                <p>{{4 * service.meeting|int}} Section/Meeting In a Month</p>
                                <hr>
                                <p>Please note that this consist of 4 major courses e.g Maths ,English, Physics and Chemistry</p>
                                <hr>
                                <p style="color:#d29948; font-weight: bold">N 45,000 / Month</p>
                                <p> <a href="#" class="btn btn-common capitalize" style="border-color:#d29948; padding: 10px 10px; margin: 5px"> <img src="/static/images/new/debit-card.png" style="width:20px; height:20px"> Subscribe for service </a></p>
                            </center>
                            </div>

                 
                            </div>