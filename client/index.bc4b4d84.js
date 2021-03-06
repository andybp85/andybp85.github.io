import { S as SvelteComponentDev, i as init, d as dispatch_dev, s as safe_not_equal, t as text, e as element, a as space, f as claim_text, c as claim_element, b as children, g as detach_dev, h as claim_space, l as add_location, j as attr_dev, m as insert_dev, o as append_dev, n as noop } from './index.ed15f1b0.js';

/* src/routes/index.svelte generated by Svelte v3.12.1 */

const file = "src/routes/index.svelte";

function create_fragment(ctx) {
	var t0, div2, div1, p, t1, t2, div0, a0, img0, t3, a1, img1, t4, a2, img2, t5, img3;

	const block = {
		c: function create() {
			t0 = text("\n\nHiya!\n\n");
			div2 = element("div");
			div1 = element("div");
			p = element("p");
			t1 = text("I'm Andy, a software engineer and musician living my dreams in Jersey City, NJ. I have a ton of interests\n            and always have several side projects going. This is my place to share my work and ideas with the world.");
			t2 = space();
			div0 = element("div");
			a0 = element("a");
			img0 = element("img");
			t3 = space();
			a1 = element("a");
			img1 = element("img");
			t4 = space();
			a2 = element("a");
			img2 = element("img");
			t5 = space();
			img3 = element("img");
			this.h();
		},

		l: function claim(nodes) {
			t0 = claim_text(nodes, "\n\nHiya!\n\n");

			div2 = claim_element(nodes, "DIV", { class: true }, false);
			var div2_nodes = children(div2);

			div1 = claim_element(div2_nodes, "DIV", { class: true }, false);
			var div1_nodes = children(div1);

			p = claim_element(div1_nodes, "P", {}, false);
			var p_nodes = children(p);

			t1 = claim_text(p_nodes, "I'm Andy, a software engineer and musician living my dreams in Jersey City, NJ. I have a ton of interests\n            and always have several side projects going. This is my place to share my work and ideas with the world.");
			p_nodes.forEach(detach_dev);
			t2 = claim_space(div1_nodes);

			div0 = claim_element(div1_nodes, "DIV", { class: true }, false);
			var div0_nodes = children(div0);

			a0 = claim_element(div0_nodes, "A", { class: true, href: true }, false);
			var a0_nodes = children(a0);

			img0 = claim_element(a0_nodes, "IMG", { alt: true, src: true, class: true }, false);
			var img0_nodes = children(img0);

			img0_nodes.forEach(detach_dev);
			a0_nodes.forEach(detach_dev);
			t3 = claim_space(div0_nodes);

			a1 = claim_element(div0_nodes, "A", { href: true, class: true }, false);
			var a1_nodes = children(a1);

			img1 = claim_element(a1_nodes, "IMG", { alt: true, src: true }, false);
			var img1_nodes = children(img1);

			img1_nodes.forEach(detach_dev);
			a1_nodes.forEach(detach_dev);
			t4 = claim_space(div0_nodes);

			a2 = claim_element(div0_nodes, "A", { href: true, class: true }, false);
			var a2_nodes = children(a2);

			img2 = claim_element(a2_nodes, "IMG", { alt: true, src: true }, false);
			var img2_nodes = children(img2);

			img2_nodes.forEach(detach_dev);
			a2_nodes.forEach(detach_dev);
			div0_nodes.forEach(detach_dev);
			div1_nodes.forEach(detach_dev);
			t5 = claim_space(div2_nodes);

			img3 = claim_element(div2_nodes, "IMG", { class: true, alt: true, src: true }, false);
			var img3_nodes = children(img3);

			img3_nodes.forEach(detach_dev);
			div2_nodes.forEach(detach_dev);
			this.h();
		},

		h: function hydrate() {
			document.title = "Andy's Site";
			add_location(p, file, 44, 8, 902);
			attr_dev(img0, "alt", "andy's Github");
			attr_dev(img0, "src", "GitHub-Mark-32px.png");
			attr_dev(img0, "class", "svelte-17uzq8p");
			add_location(img0, file, 51, 16, 1274);
			attr_dev(a0, "class", "github-andybp85 svelte-17uzq8p");
			attr_dev(a0, "href", "https://github.com/andybp85");
			add_location(a0, file, 50, 12, 1195);
			attr_dev(img1, "alt", "andy's Github");
			attr_dev(img1, "src", "f_logo_RGB-Blue_1024.png");
			add_location(img1, file, 54, 16, 1423);
			attr_dev(a1, "href", "https://www.facebook.com/andrew.stanish");
			attr_dev(a1, "class", "svelte-17uzq8p");
			add_location(a1, file, 53, 12, 1356);
			attr_dev(img2, "alt", "andy's Github");
			attr_dev(img2, "src", "Twitter_Social_Icon_Rounded_Square_Color.png");
			add_location(img2, file, 57, 16, 1565);
			attr_dev(a2, "href", "https://twitter.com/andybp85");
			attr_dev(a2, "class", "svelte-17uzq8p");
			add_location(a2, file, 56, 12, 1509);
			attr_dev(div0, "class", "links svelte-17uzq8p");
			add_location(div0, file, 49, 8, 1163);
			attr_dev(div1, "class", "intro svelte-17uzq8p");
			add_location(div1, file, 43, 4, 874);
			attr_dev(img3, "class", "me svelte-17uzq8p");
			attr_dev(img3, "alt", "me");
			attr_dev(img3, "src", "me.jpg");
			add_location(img3, file, 63, 4, 1691);
			attr_dev(div2, "class", "wrapper svelte-17uzq8p");
			add_location(div2, file, 42, 0, 848);
		},

		m: function mount(target, anchor) {
			insert_dev(target, t0, anchor);
			insert_dev(target, div2, anchor);
			append_dev(div2, div1);
			append_dev(div1, p);
			append_dev(p, t1);
			append_dev(div1, t2);
			append_dev(div1, div0);
			append_dev(div0, a0);
			append_dev(a0, img0);
			append_dev(div0, t3);
			append_dev(div0, a1);
			append_dev(a1, img1);
			append_dev(div0, t4);
			append_dev(div0, a2);
			append_dev(a2, img2);
			append_dev(div2, t5);
			append_dev(div2, img3);
		},

		p: noop,
		i: noop,
		o: noop,

		d: function destroy(detaching) {
			if (detaching) {
				detach_dev(t0);
				detach_dev(div2);
			}
		}
	};
	dispatch_dev("SvelteRegisterBlock", { block, id: create_fragment.name, type: "component", source: "", ctx });
	return block;
}

class Index extends SvelteComponentDev {
	constructor(options) {
		super(options);
		init(this, options, null, create_fragment, safe_not_equal, []);
		dispatch_dev("SvelteRegisterComponent", { component: this, tagName: "Index", options, id: create_fragment.name });
	}
}

export default Index;
