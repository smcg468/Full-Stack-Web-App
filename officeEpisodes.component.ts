import { Component, OnInit } from '@angular/core';
import { WebService } from '../web.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'officeEpisodes',
  templateUrl: './officeEpisodes.component.html',
  styleUrls: ['./officeEpisodes.component.css']
})
export class OfficeEpisodesComponent {

  constructor(public webService: WebService,
               public route: ActivatedRoute){
  }


  ngOnInit() {
      console.log("nginit")
      this.webService.getOfficeEpisodes(this.page);
  }
  
  previousPage(){
      if (this.page > 1){
          this.page = this.page - 1;
          this.episodes_list = this.webService.getOfficeEpisodes(this.page);
      }
  }

  nextPage(){
      this.page = this.page + 1;
      this.episodes_list = this.webService.getOfficeEpisodes(this.page);
  }


  page: number = 1;
  episodes_list: any = [];


}
