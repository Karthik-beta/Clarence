import { Component, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared.service';

@Component({
  selector: 'app-addshiftmanagement',
  templateUrl: './addshiftmanagement.component.html',
  styleUrls: ['./addshiftmanagement.component.css']
})
export class AddshiftmanagementComponent implements OnInit {

  constructor(private service:SharedService) { }

  ProductionPlanList:any=[];
  ModalTitle:string="";
  ActivateAddEditProdPlanComp:boolean=false;
  prodplan:any;
  searchText:string="";
  ProductionPlanListWithoutFilter:any=[];


  ngOnInit(): void {
  }


  selectedEmployee: string='';

  employeeOptions: string[] = [
    'Meshak, 223044347',
    'Ramachandra G, 305020222',
    'Raja Shankara G, 305022167',
    'Nagendra Swamy C G, 305021393',
    // Add more employee options here if needed
  ];

}
