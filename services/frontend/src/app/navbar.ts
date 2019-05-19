// guest.guard.ts

import { Injectable } from '@angular/core';

@Injectable()
export class Navbar{

  public visible: boolean;

  constructor() { this.visible = false; }

  hide() { this.visible = false; }

  show() { this.visible = true; }

  toggle() { this.visible = !this.visible; }

}
